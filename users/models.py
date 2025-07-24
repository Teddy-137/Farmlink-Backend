from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if (
            not extra_fields.get("is_superuser")
            and not extra_fields.get("is_staff")
            and not extra_fields.get("role")
        ):
            raise ValueError("Role is required for non-superuser/non-staff users.")
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields["role"] = None
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ("producer", "Producer"),
        ("consumer", "Consumer"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.is_superuser and not self.is_staff and not self.role:
            raise ValueError("Role is required for non-superuser/non-staff users.")
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name="profile"
    )
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
