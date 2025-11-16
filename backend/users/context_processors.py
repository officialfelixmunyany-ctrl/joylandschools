"""Removed site-status runtime behaviour.

This context processor now returns a simple default payload to keep
templates referencing `site_status` from breaking. The site-status
feature (DB model, JSON fallback, JS UI) was intentionally removed in
cleanup; this function preserves a stable contract for templates.
"""

from django.utils import timezone
from core.models import Presence, DailyPresence
import datetime


def site_status(request):
    return {
        'site_status': {
            'status': 'waiting',
            'label': 'Waiting',
            'message': 'Site status unknown',
            'color': '#6c757d',
        }
    }


def presence_stats(request):
    """Context processor returning simple presence metrics:
    - current_online: users with last_seen within PRESENCE_WINDOW_MINUTES (default 5)
    - today_unique: distinct identifiers recorded for today
    - today_peak: recorded peak concurrent for today
    """
    now = timezone.now()
    today = now.date()
    window = now - datetime.timedelta(minutes=5)

    try:
        # Only count authenticated users as online
        current_online = Presence.objects.filter(last_seen__gte=window, user__isnull=False).count()
    except Exception:
        current_online = 0

    try:
        today_unique = Presence.objects.filter(date=today).count()
    except Exception:
        today_unique = 0

    try:
        dp = DailyPresence.objects.filter(date=today).first()
        today_peak = dp.peak if dp else 0
    except Exception:
        today_peak = 0

    return {
        'presence_stats': {
            'current_online': current_online,
            'today_unique': today_unique,
            'today_peak': today_peak,
        }
    }
