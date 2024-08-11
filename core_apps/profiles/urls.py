from django.urls import path
from .views import (AvatarUploadView, ProfileDetailAPIView, ProfileUpdateAPIView, ProfileListAPIView, NonTenantProfileListAPIView)

urlpatterns = [
  path("all/", ProfileListAPIView.as_view(), name="profile-list"),
  path("non-tenant-profiles/", NonTenantProfileListAPIView.as_view(), name="non-tenant-list"),
  path("user/my-profile/", ProfileDetailAPIView.as_view(), name="profile-detail"),
  path("user/update/", ProfileUpdateAPIView.as_view(), name="profile-update"),
  path("user/avatar/", AvatarUploadView.as_view(), name="avatar-upload"),
]
