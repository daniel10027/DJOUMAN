from typing import Optional
from infrastructure.persistence.models import WebhookEvent

class EventRepository:
    def get_or_create_event(self, source: str, event_id: str, signature: str | None, payload: dict) -> tuple[WebhookEvent, bool]:
        obj, created = WebhookEvent.objects.get_or_create(
            source=source, event_id=event_id,
            defaults={"signature": signature, "payload": payload}
        )
        return obj, created

    def mark_processed(self, event: WebhookEvent) -> WebhookEvent:
        from django.utils import timezone
        event.status = "processed"
        event.processed_at = timezone.now()
        event.save(update_fields=["status","processed_at"])
        return event

    def mark_error(self, event: WebhookEvent) -> WebhookEvent:
        event.status = "error"
        event.save(update_fields=["status"])
        return event
