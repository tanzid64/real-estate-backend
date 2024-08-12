from typing import Any
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from core_apps.common.renderers import GenericJSONRenderer
from core_apps.profiles.models import Profile
from core_apps.apartments.models import Apartment
from core_apps.apartments.serializers import ApartmentSerializer

class ApartmentCreateAPIView(generics.CreateAPIView):
  queryset = Apartment.objects.all()
  serializer_class = ApartmentSerializer
  renderer_classes = [GenericJSONRenderer]
  object_label = "apartment"

  def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    user = request.user
    if user.is_superuser or (hasattr(user, "profile") and user.profile.occupation == Profile.Occupation.TENANT):
      return super().create(request, *args, **kwargs)

    return Response({"message": "You are not allowed to create an apartment, you are not a tenant"},status=status.HTTP_403_FORBIDDEN)
  
class ApartmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ApartmentSerializer
  renderer_classes = [GenericJSONRenderer]
  object_label = "apartment"

  def get_object(self) -> Apartment:
    queryset = self.request.user.apartment.all()
    obj = generics.get_object_or_404(queryset)
    return obj
