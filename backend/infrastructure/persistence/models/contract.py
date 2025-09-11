from django.db import models

class Contract(models.Model):
    booking = models.OneToOneField("persistence.Booking", on_delete=models.CASCADE, related_name="contract")
    file_url = models.URLField()
    signed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Contract#{self.pk}"
