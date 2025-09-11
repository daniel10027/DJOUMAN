from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import secrets

class AuthOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=16, choices=[("login","login"),("reset","reset")])
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_for(user_id: int, purpose: str = "login", ttl_minutes: int = 10):
        code = f"{secrets.randbelow(1000000):06d}"
        obj = AuthOTP.objects.create(
            user_id=user_id, code=code, purpose=purpose, expires_at=timezone.now()+timedelta(minutes=ttl_minutes)
        )
        return obj
