from django.urls import path
from .views import (
  IssueListAPIView,
  IssueDetailAPIView,
  IssueCreateAPIView,
  IssueUpdateAPIView,
  IssueDeleteAPIView,
  MyIssuesListAPIView,
  AssignedIssuesListView
)

urlpatterns = [
  path("", IssueListAPIView.as_view(), name="issue-list"),
  path("me/", MyIssuesListAPIView.as_view(), name="my-issues-list"),
  path("assigned/", AssignedIssuesListView.as_view(), name="assigned-issues-list"),
  path("create/<uuid:appartment_id>/", IssueCreateAPIView.as_view(), name="issue-create"),
  path("update/<uuid:id>/", IssueUpdateAPIView.as_view(), name="issue-update"),
  path("<uuid:id>/", IssueDetailAPIView.as_view(), name="issue-detail"),
  path("delete/<uuid:id>/", IssueDeleteAPIView.as_view(), name="issue-delete"),
]
