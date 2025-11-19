"""Email alert system for sending notifications to distribution lists"""

import logging
from django.core.mail import send_mail
from django.conf import settings
from .models import AlertType

logger = logging.getLogger(__name__)


def send_alert_email(alert_type_key, subject, message, fail_silently=True):
    """
    Send an email alert to all subscribed recipients for a given alert type.

    Args:
        alert_type_key: The alert_type field value (e.g., 'new_inquiry')
        subject: Email subject line
        message: Email message body
        fail_silently: Whether to suppress email sending errors

    Returns:
        tuple: (success: bool, recipients: list, error: str or None)
    """
    try:
        # Get the alert type
        alert = AlertType.objects.filter(alert_type=alert_type_key, is_active=True).first()

        if not alert:
            logger.warning(f"Alert type '{alert_type_key}' not found or not active. Email not sent.")
            return (False, [], f"Alert type '{alert_type_key}' not configured or disabled")

        # Get active recipients
        recipients = alert.get_active_recipients()

        if not recipients:
            logger.warning(f"No active recipients for alert '{alert_type_key}'. Email not sent.")
            return (False, [], "No active recipients configured for this alert")

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=fail_silently,
        )

        logger.info(f"Alert '{alert_type_key}' sent to {len(recipients)} recipients: {', '.join(recipients)}")
        return (True, recipients, None)

    except Exception as e:
        logger.error(f"Error sending alert '{alert_type_key}': {str(e)}")
        if fail_silently:
            return (False, [], str(e))
        else:
            raise


def get_alert_recipients(alert_type_key):
    """
    Get list of active recipients for a given alert type.

    Args:
        alert_type_key: The alert_type field value (e.g., 'new_inquiry')

    Returns:
        list: Email addresses of active recipients
    """
    try:
        alert = AlertType.objects.filter(alert_type=alert_type_key, is_active=True).first()
        if alert:
            return alert.get_active_recipients()
        return []
    except Exception as e:
        logger.error(f"Error getting recipients for alert '{alert_type_key}': {str(e)}")
        return []
