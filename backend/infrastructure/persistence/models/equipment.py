from django.db import models
from django.conf import settings

class Equipment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="equipments")
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default="XOF")
    photos = models.JSONField(blank=True, null=True, help_text="Liste d'URLs")
    availability_notes = models.CharField(max_length=255, blank=True, null=True)
    geo_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    geo_lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
