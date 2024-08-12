import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL

from .models import Issue

logger = logging.getLogger(__name__)

def send_issue_confirmation_email(issue: Issue) -> None:
  try:
    subject = "Issue Report Confirmation"
    context = {"issue": issue, "site_name": SITE_NAME}
    html_message = render_to_string("emails/issue_confirmation.html", context)
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL
    to = [issue.reported_by.email]
    email = EmailMultiAlternatives(subject, plain_message, from_email, to)
    email.attach_alternative(html_message, "text/html")
    email.send()
  except Exception as e:
    logger.error(f"Failed to send confirmation email for issue '{issue.title}:{e}'", exc_info=True)

def send_issue_resolved_email(issue: Issue) -> None:
  try:
    subject = "Issue Resolved"
    context = {"issue": issue, "site_name": SITE_NAME}
    html_message = render_to_string("emails/issue_resolved_notification.html", context)
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL
    to = [issue.reported_by.email]
    email = EmailMultiAlternatives(subject, plain_message, from_email, to)
    email.attach_alternative(html_message, "text/html")
    email.send()
  except Exception as e:
    logger.error(f"Failed to send resolution email for issue '{issue.title}:{e}'", exc_info=True)

def send_resolution_email(issue: Issue) -> None:
  try:
    subject = f"Issue Resolved: {issue.title}"
    context = {"issue": issue, "site_name": SITE_NAME}
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [issue.reported_by.email]
    html_message = render_to_string("emails/issue_resolved_notification.html", context)
    plain_message = strip_tags(html_message)
    email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")
    email.send()
  except Exception as e:
    logger.error(f"Failed to send resolution email for issue '{issue.title}:{e}'", exc_info=True)