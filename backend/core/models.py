from __future__ import annotations
from django.db import models
from django.utils import timezone


class AnnouncementManager(models.Manager):
    """Manager for Announcement model providing common queries."""

    def get_active_for_landing(self) -> models.QuerySet:
        return self.filter(is_active=True).order_by('priority', '-created_at')[:5]

    def get_archive_list(self) -> models.QuerySet:
        return self.filter(is_active=False).order_by('priority', '-created_at')


class Announcement(models.Model):
    title = models.CharField(max_length=140)
    message = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveSmallIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    objects: AnnouncementManager = AnnouncementManager()

    class Meta:
        ordering = ['priority', '-created_at']

    def __str__(self) -> str:
        return self.title

    def short_message(self, length: int = 100) -> str:
        if len(self.message) <= length:
            return self.message
        return f"{self.message[:length-3]}..."


class RegistrationRequest(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    user_type = models.CharField(max_length=16, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    country_code = models.CharField(max_length=8, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    address = models.TextField(blank=True)
    birth_month = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_day = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    heard_about = models.CharField(max_length=255, blank=True)
    agree = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['user_type', 'status']),
        ]

    def __str__(self) -> str:
        return f"{self.get_user_type_display()} request from {self.first_name} {self.last_name} <{self.email}>"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


class Presence(models.Model):
    identifier = models.CharField(max_length=128, db_index=True)
    last_seen = models.DateTimeField(auto_now=True)
    date = models.DateField(db_index=True)

    class Meta:
        unique_together = (('identifier', 'date'),)

    def __str__(self) -> str:
        return f"{self.identifier} @ {self.last_seen.isoformat()} ({self.date})"


class DailyPresence(models.Model):
    date = models.DateField(unique=True)
    peak = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.date}: peak={self.peak}"


class EventManager(models.Manager):
    def upcoming(self, limit: int = 10):
        return self.filter(start__gte=timezone.now(), is_public=True).order_by('start')[:limit]


class Event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects: EventManager = EventManager()

    class Meta:
        ordering = ['start']

    def __str__(self) -> str:
        return f"{self.title} ({self.start.date().isoformat()})"
