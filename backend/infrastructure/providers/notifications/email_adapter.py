import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailAdapter:
    def send_email(self, to: str, subject: str, html: str) -> None:
        try:
            send_mail(
                subject,
                "",
                settings.DEFAULT_FROM_EMAIL,
                [to],
                html_message=html,
                fail_silently=False,
            )
        except Exception as e:
            logger.exception("Email sending failed: %s", e)
