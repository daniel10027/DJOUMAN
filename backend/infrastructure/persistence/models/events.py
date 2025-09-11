from django.db import models

class WebhookEvent(models.Model):
    """
    Journal/idempotence pour webhooks externes.
    """
    source = models.CharField(max_length=32)  # wave|stripe|om|mtn
    event_id = models.CharField(max_length=128, db_index=True)
    signature = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=16, default="received")  # received|processed|error
    payload = models.JSONField()
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("source","event_id")]

    def __str__(self):
        return f"{self.source}:{self.event_id} ({self.status})"
