import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class SmsAdapter:
    def send_sms(self, to: str, message: str) -> None:
        provider_url = getattr(settings, "SMS_API_URL", None)
        api_key = getattr(settings, "SMS_API_KEY", None)
        if not provider_url or not api_key:
            logger.warning("SMS provider not configured")
            return
        try:
            requests.post(provider_url, json={"to": to, "text": message, "api_key": api_key}, timeout=5)
        except Exception as e:
            logger.exception("SMS send error: %s", e)
