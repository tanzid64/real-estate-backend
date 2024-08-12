from email.policy import default
import logging
from typing import Any

from django.http import Http404
from django.utils import timezone
from requests import delete
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied, ValidationError

from core_apps.apartments.models import Apartment
from core_apps.common.models import ContentView
from core_apps.common.renderers import GenericJSONRenderer
from .emails import send_issue_confirmation_email, send_issue_resolved_email
from .models import Issue
from .serializers import (
  IssueSerializer,
  IssueStatusUpdateSerializer
)
from django.contrib.contenttypes.models import ContentType
logger = logging.getLogger(__name__)

class IsStaffOrSuperUser(permissions.BasePermission):
  def __init__(self) -> None:
    self.message = None
  def has_permission(self, request, view):
    is_authorized = (request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))
    if not is_authorized:
      self.message = "Access Denied. Restricted to staff or admin users only."
    return is_authorized
  
class IssueListAPIView(generics.ListAPIView):
  queryset = Issue.objects.all()
  serializer_class = IssueSerializer
  renderer_classes = [GenericJSONRenderer]
  permission_classes = [IsStaffOrSuperUser]
  object_label = "issue"

class AssignedIssuesListView(generics.ListAPIView):
  serializer_class = IssueSerializer
  renderer_classes = [GenericJSONRenderer]
  object_label = "issue"

  def get_queryset(self):
    user = self.request.user
    return Issue.objects.filter(assigned_to=user)
  
class MyIssuesListAPIView(generics.ListAPIView):
  queryset = Issue.objects.all()
  serializer_class = IssueSerializer
  renderer_classes = [GenericJSONRenderer]
  object_label = "my_issue"

  def get_queryset(self):
    user = self.request.user
    return Issue.objects.filter(reported_by=user)
  
class IssueCreateAPIView(generics.CreateAPIView):
  queryset = Issue.objects.all()
  serializer_class = IssueSerializer
  renderer_classes = [GenericJSONRenderer]
  object_label = "issue"

  def perform_create(self, serializer: IssueSerializer) -> None:
    apartment_id = self.kwargs.get("apartment_id")
    if not apartment_id:
      raise ValidationError({"apartment_id": ["Apartment ID is required"]})
    try:
      apartment = Apartment.objects.get(id=apartment_id, tenant = self.request.user)
    except Apartment.DoesNotExist:
      raise PermissionDenied("You do not have permission to create an issue for this apartment")
    issue = serializer.save(reported_by=self.request.user, apartment=apartment)
    send_issue_confirmation_email(issue)

class IssueDetailAPIView(generics.RetrieveAPIView):
  queryset = Issue.objects.all()
  serializer_class = IssueSerializer
  lookup_field = "id"
  renderer_classes = [GenericJSONRenderer]
  object_label = "issue"

  def get_object(self) -> Issue:
    issue = super().get_object()
    user = self.request.user
    if not (
      user == issue.reported_by or
      user == issue.assigned_to or
      user.is_staff or
      user.is_superuser
    ):
      raise PermissionDenied("You do not have permission to view this issue") 
    
    self.record_issue_view(issue)
    return issue
  
  def record_issue_view(self, issue: Issue) -> None:
    content_type = ContentType.objects.get_for_model(issue)
    viewer_ip = self.get_client_ip()
    user = self.request.user
    obj, created = ContentView.objects.update_or_create(
      content_type = content_type,
      object_id = issue.pk,
      user = user,
      viewer_ip = viewer_ip,
      default = {
        "last_viewed": timezone.now()
      }
    )

  def get_client_ip(self) -> str:
    x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
      ip = x_forwarded_for.split(',')[0]
    else:
      ip = self.request.META.get('REMOTE_ADDR')
    return ip
  

  class IssueUpdateAPIView(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueStatusUpdateSerializer
    lookup_field = "id"
    renderer_classes = [GenericJSONRenderer]
    object_label = "issue"

    def get_object(self) -> Issue:
      issue = super().get_object()
      user = self.request.user
      if not (
        user == issue.assigned_to or
        user.is_staff or
        user.is_superuser
      ):
        logger.warning(f"User {user.get_full_name} does not have permission to update issue {issue.id}")
        raise PermissionDenied("You do not have permission to update this issue") 
      send_issue_resolved_email(issue)
      return issue
    
class IssueDeleteAPIView(generics.DestroyAPIView):
  queryset = Issue.objects.all()
  serializer_class = IssueSerializer
  lookup_field = "id"

  def get_object(self) -> Issue:
    try:
      issue = super().get_object()
    except Http404:
      raise Http404("Issue not found")
    
    user = self.request.user
    if not (
      user == issue.reported_by or
      user.is_staff or
      user.is_superuser
    ):
      logger.warning(f"User {user.get_full_name} does not have permission to delete issue {issue.id}")
      raise PermissionDenied("You do not have permission to delete this issue") 
    return issue
  
  def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    super().delete(request, *args, **kwargs)
    return Response(status=status.HTTP_204_NO_CONTENT)