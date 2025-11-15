from __future__ import annotations
from typing import Optional, Any
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
import uuid


class CustomUserManager(UserManager):
    def create_superuser(self, username: str, email: Optional[str] = None, password: Optional[str] = None, **extra_fields: Any):
        extra_fields.setdefault('role', 'system_admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('system_admin', 'System Administrator'),
        ('principal', 'Principal'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('account', 'Account'),
    ]

    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='student')
    objects: CustomUserManager = CustomUserManager()

    def get_role_display_name(self) -> str:
        return dict(self.ROLE_CHOICES).get(self.role, self.role)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    assessment_number = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    admission_number = models.CharField(max_length=64, unique=True, blank=True, db_index=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.admission_number:
            self.admission_number = f"AD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.admission_number}"


# Proxy models for admin separation
class StaffProfile(User):
    class Meta:
        proxy = True
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'


class PrincipalProfile(User):
    class Meta:
        proxy = True
        verbose_name = 'Principal Profile'
        verbose_name_plural = 'Principal Profiles'


# The following models were moved to the new `core` app for better separation of concerns:
# - Announcement
# - RegistrationRequest
# - Presence
# - DailyPresence
# - Event
# Please see `core/models.py` for their definitions and update migrations accordingly.
