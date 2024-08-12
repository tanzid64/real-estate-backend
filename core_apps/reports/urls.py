from django.urls import path
from .views import (
  ReportListAPIView,
  ReportCreateAPIView
)

urlpatterns = [
  path("create/", ReportCreateAPIView.as_view(), name="report-create"),
  path("me/", ReportListAPIView.as_view(), name="report-list"),
]