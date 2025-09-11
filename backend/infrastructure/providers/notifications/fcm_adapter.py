import logging, requests
from django.conf import settings
from infrastructure.persistence.repositories.device_repository import DeviceRepository

logger = logging.getLogger(__name__)

class FcmAdapter:
    def __init__(self):
        self.server_key = getattr(settings, "FCM_KEY", None)
        self.url = "https://fcm.googleapis.com/fcm/send"

    def _headers(self):
        return {"Authorization": f"key={self.server_key}", "Content-Type": "application/json"}

    def send_push(self, user_id: int, title: str, body: str, data: dict | None = None) -> None:
        if not self.server_key:
            logger.warning("FCM_KEY not set"); return
        tokens = [d.token for d in DeviceRepository().list_by_user(user_id)]
        if not tokens:
            logger.info("No device tokens for user %s", user_id)
            return
        for tk in tokens:
            payload = {"to": tk, "notification": {"title": title, "body": body}, "data": data or {}}
            try:
                requests.post(self.url, json=payload, headers=self._headers(), timeout=5)
            except Exception as e:
                logger.exception("Push send error: %s", e)
