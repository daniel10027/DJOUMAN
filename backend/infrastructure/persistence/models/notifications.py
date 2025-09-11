from django.db import models
from django.conf import settings

class DeviceToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="device_tokens")
    platform = models.CharField(max_length=16, choices=[("android","Android"), ("ios","iOS"), ("web","Web")])
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id}:{self.platform}"
