from django.db import models
from django.conf import settings

class BookingStatus(models.TextChoices):
    DRAFT = "draft", "Brouillon"
    PENDING = "pending", "En attente"
    CONFIRMED = "confirmed", "Confirmée"
    CANCELLED = "cancelled", "Annulée"
    COMPLETED = "completed", "Terminée"

class Booking(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    service = models.ForeignKey("persistence.Service", on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    equipment = models.ForeignKey("persistence.Equipment", on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    status = models.CharField(max_length=16, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default="XOF")
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # %
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Booking#{self.pk} ({self.status})"
