from django.contrib import admin
from django.db.models import Queryset
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Report
# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
  list_display = ("title", "reported_by", "reported_user", "get_report_count", "created_at")
  search_fields = (
    "title",
    "reported_by__username",
    "reported_user__username",
  )
  def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    return super().get_queryset(request).select_related("reported_user__profile")
  
  def get_report_count(self, obj: Report) -> int:
    return obj.reported_user.profile.report_count
  
  get_report_count.short_description = "Report Count"
