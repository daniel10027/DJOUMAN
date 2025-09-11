from django.db import models

class PaymentMethod(models.TextChoices):
    ORANGE = "orange_money", "Orange Money"
    MTN = "mtn_momo", "MTN MoMo"
    WAVE = "wave", "Wave"
    STRIPE = "stripe", "Stripe"

class PaymentStatus(models.TextChoices):
    REQUIRES_ACTION = "requires_action", "Requires action"
    PENDING = "pending", "Pending"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"

class Payment(models.Model):
    booking = models.ForeignKey("persistence.Booking", on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(max_length=24, choices=PaymentMethod.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="XOF")
    fees = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=24, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    provider_ref = models.CharField(max_length=120, blank=True, null=True)
    idempotency_key = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Payment#{self.pk} {self.amount} {self.currency} ({self.status})"
