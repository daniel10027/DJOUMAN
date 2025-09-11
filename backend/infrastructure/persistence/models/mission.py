from django.db import models
from django.conf import settings

class MissionStatus(models.TextChoices):
    CREATED = "created", "Créée"
    ACCEPTED = "accepted", "Acceptée"
    STARTED = "started", "Démarrée"
    PAUSED = "paused", "En pause"
    STOPPED = "stopped", "Arrêtée"
    COMPLETED = "completed", "Terminée"

class Mission(models.Model):
    booking = models.OneToOneField("persistence.Booking", on_delete=models.CASCADE, related_name="mission")
    freelance = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="missions")
    status = models.CharField(max_length=16, choices=MissionStatus.choices, default=MissionStatus.CREATED)

    started_at = models.DateTimeField(null=True, blank=True)
    paused_at = models.DateTimeField(null=True, blank=True)
    stopped_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    gps_track = models.JSONField(blank=True, null=True)
    proofs = models.JSONField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Mission#{self.pk} ({self.status})"
