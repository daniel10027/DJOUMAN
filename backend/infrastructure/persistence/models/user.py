from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    CLIENT = "client", "Client"
    FREELANCE = "freelance", "Freelance"
    OWNER = "owner", "Propriétaire/Loueur"
    ADMIN = "admin", "Admin"

class UserStatus(models.TextChoices):
    ACTIVE = "active", "Actif"
    INACTIVE = "inactive", "Inactif"
    SUSPENDED = "suspended", "Suspendu"

class User(AbstractUser):
    """
    Utilisateur principal.
    Champs hérités : username, password, first_name, last_name, email, is_staff, is_active, date_joined...
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    role = models.CharField(max_length=16, choices=UserRole.choices, default=UserRole.CLIENT)
    status = models.CharField(max_length=16, choices=UserStatus.choices, default=UserStatus.ACTIVE)
    date_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

class Profile(models.Model):
    """Profil public basique."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=120, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    geo_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    geo_lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self) -> str:
        return self.name or f"Profile#{self.pk}"
