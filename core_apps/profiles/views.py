from typing import List
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from yaml import serialize
from core_apps.common.renderers import GenericJSONRenderer
from core_apps.profiles.tasks import upload_avatar_to_cloudinary
from .models import Profile
from .serializers import (AvatarUploadSerializer, ProfileSerializer, UpdateProfileSerializer)

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
  page_size = 9
  page_size_query_param = 'page_size'
  max_page_size = 100

class ProfileListAPIView(generics.ListAPIView):
  serializer_class = ProfileSerializer
  renderer_classes = [GenericJSONRenderer]
  pagination_class = StandardResultsSetPagination
  object_label = "profiles"
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
  search_fields = ["user__username", "user__first_name", "user__last_name"]
  filterset_fields = ["occupation", "gender", "country_of_origin"]

  def get_queryset(self) -> List:
      return Profile.objects.exclude(user__is_staff=True).exclude(user__is_superuser=True).filter(occupation=Profile.Occupation.TENANT)


class ProfileDetailAPIView(generics.RetrieveAPIView):
  serializer_class = ProfileSerializer
  renderer_classes = [GenericJSONRenderer]
  object_label = "profile"
  def get_queryset(self) -> QuerySet:
    return Profile.objects.select_related("user").all()
  def get_object(self) -> Profile:
    try:
      return Profile.objects.get(user=self.request.user)
    except Profile.DoesNotExist:
      raise Http404("Profile not found")
    
class ProfileUpdateAPIView(generics.UpdateAPIView):
  serializer_class = UpdateProfileSerializer
  renderer_classes = [GenericJSONRenderer]
  object_label = "profile"
  def get_queryset(self):
    return Profile.objects.none()
  def get_object(self) -> Profile:
    try:
      return Profile.objects.get(user=self.request.user)
    except Profile.DoesNotExist:
      raise Http404("Profile not found")
    
  def perform_update(self, serializer: UpdateProfileSerializer):
    data = serializer.validate.pop("user", {})
    profile = serializer.save()
    User.objects.filter(id=self.request.user.id).update(**data)
    return profile
  
class AvatarUploadView(APIView):
  def patch(self, request, *args, **kwargs):
    return self.upload_avatar(request, *args, **kwargs)
  
  def upload_avatar(self, request, *args, **kwargs):
    profile = request.user.profile
    serialize = AvatarUploadSerializer(profile, data=request.data)

    if serialize.is_valid():
      image = serialize.validated_data["avatar"]
      content = image.read()
      upload_avatar_to_cloudinary.delay(profile.id, content)
      return Response(
        {"message": "Avatar upload started"}, status = status.HTTP_202_ACCEPTED
      )
    
    return Response(serialize.errors, status = status.HTTP_400_BAD_REQUEST)

class NonTenantProfileListAPIView(generics.ListAPIView):
  serializer_class = ProfileSerializer
  renderer_classes = [GenericJSONRenderer]
  pagination_class = StandardResultsSetPagination
  object_label = "non_tenant_profiles"
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
  search_fields = ["user__username", "user__first_name", "user__last_name"]
  filterset_fields = ["occupation", "gender", "country_of_origin"]

  def get_queryset(self) -> List:
      return Profile.objects.exclude(user__is_staff=True).exclude(user__is_superuser=True).exclude(occupation=Profile.Occupation.TENANT)