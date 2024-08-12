from rest_framework import generics, serializers
from .models import Report
from core_apps.common.renderers import GenericJSONRenderer
from .serializers import ReportSerializer

class ReportCreateAPIView(generics.CreateAPIView):
  queryset = Report.objects.all()
  serializer_class = ReportSerializer
  renderer_class = [GenericJSONRenderer]
  object_label = "report"

  def perform_create(self, serializer: serializers.Serializer ) -> None:
    serializer.save(reported_by=self.request.user)

class ReportListAPIView(generics.ListAPIView):
  queryset = Report.objects.all()
  serializer_class = ReportSerializer
  renderer_class = [GenericJSONRenderer]
  object_label = "reports"

  def get_queryset(self) -> Report:
    user = self.request.user
    return Report.objects.filter(reported_by=user)
