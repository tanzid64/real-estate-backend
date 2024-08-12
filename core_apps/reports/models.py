from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from core_apps.common.models import TimeStampedModel
# Create your models here.

User = get_user_model()

class Report(TimeStampedModel):
  title = models.CharField(verbose_name=_("Title"), max_length=255)
  slug = AutoSlugField(populate_from="title", unique=True)
  reported_by = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="reports_made",
    verbose_name=_("Reported By")
  )
  reported_user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="reports_received",
    verbose_name=_("Reported User")
  )
  description = models.TextField(verbose_name=_("Description"))

  def __str__(self) -> str:
    return f"Reported by {self.reported_by.get_full_name} against {self.reported_user.get_full_name}"

  class Meta:
    verbose_name = _("Report")
    verbose_name_plural = _("Reports")
    ordering = ("-created_at",)