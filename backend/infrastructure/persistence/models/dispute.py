from django.db import models
from django.conf import settings

class DisputeStatus(models.TextChoices):
    OPEN = "open", "Ouvert"
    IN_REVIEW = "in_review", "En revue"
    RESOLVED = "resolved", "Résolu"
    REJECTED = "rejected", "Rejeté"

class Dispute(models.Model):
    booking = models.ForeignKey("persistence.Booking", on_delete=models.CASCADE, related_name="disputes")
    opener = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="disputes_opened")
    reason = models.CharField(max_length=255)
    messages = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=DisputeStatus.choices, default=DisputeStatus.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Dispute#{self.pk} ({self.status})"
