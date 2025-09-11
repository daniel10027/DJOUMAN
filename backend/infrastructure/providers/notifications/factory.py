import os
from infrastructure.providers.notifications.fcm_adapter import FcmAdapter
from infrastructure.providers.notifications.email_adapter import EmailAdapter
from infrastructure.providers.notifications.sms_adapter import SmsAdapter
from infrastructure.providers.notifications import tasks

class NotificationFacade:
    def __init__(self):
        self.push = FcmAdapter()
        self.email = EmailAdapter()
        self.sms = SmsAdapter()
        self.async_enabled = os.getenv("CELERY_ENABLED","false").lower()=="true"

    def _maybe_async(self, fn, *args, **kwargs):
        if self.async_enabled:
            return fn.delay(*args, **kwargs)
        return fn(*args, **kwargs)

    def notify_booking_confirmed(self, user_id: int, booking_id: int):
        self._maybe_async(tasks.task_send_push, user_id, "Réservation confirmée", f"Votre réservation #{booking_id} est confirmée")

    def notify_mission_status(self, user_id: int, mission_id: int, status_label: str):
        self._maybe_async(tasks.task_send_push, user_id, "Mission", f"Mission #{mission_id} → {status_label}")
