from django.db import models

class OrganizationStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"

class Organization(models.Model):
    name = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=16, choices=OrganizationStatus.choices, default=OrganizationStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
