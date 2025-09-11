from django.db import models
from django.conf import settings

class KycStatus(models.TextChoices):
    PENDING = "pending", "En attente"
    APPROVED = "approved", "Approuvée"
    REJECTED = "rejected", "Rejetée"

class KycDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="kyc_documents")
    doc_type = models.CharField(max_length=64)  # ex: id_card, passport
    file_url = models.URLField()
    data = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=KycStatus.choices, default=KycStatus.PENDING)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="kyc_reviewed")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KYC#{self.pk} {self.doc_type} ({self.status})"
