# Generated by Django 4.2.11 on 2024-08-10 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ContentView",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField(verbose_name="Object ID")),
                (
                    "viewer_ip",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="ViewerIP Address"
                    ),
                ),
                ("ulast_viewed", models.DateTimeField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                        verbose_name="Content Type",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Content View",
                "verbose_name_plural": "Content Views",
                "unique_together": {("content_type", "object_id", "user", "viewer_ip")},
            },
        ),
    ]
