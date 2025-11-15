from __future__ import annotations
import datetime
from django.utils import timezone
from django.conf import settings

from core.models import Presence, DailyPresence


class PresenceMiddleware:
    """Middleware that records user/session activity for lightweight presence.

    Behavior:
    - Ensures the session has a key for anonymous visitors.
    - Creates/updates a Presence row for today with last_seen timestamp.
    - Computes current online (last_seen within window) and updates DailyPresence.peak.
    """

    # time window (in minutes) to consider a user "online"
    WINDOW_MINUTES = getattr(settings, 'PRESENCE_WINDOW_MINUTES', 5)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure session exists (so anonymous visitors get a session key)
        try:
            session_key = request.session.session_key
            if session_key is None:
                # creating a session if none exists
                request.session.save()
                session_key = request.session.session_key
        except Exception:
            session_key = None

        # Determine identifier
        if getattr(request, 'user', None) and request.user.is_authenticated:
            identifier = f"user:{request.user.pk}"
        elif session_key:
            identifier = f"session:{session_key}"
        else:
            identifier = None

        # Record presence for today
        if identifier:
            now = timezone.now()
            today = now.date()
            # update_or_create ensures we have one row per identifier per day
            try:
                Presence.objects.update_or_create(
                    identifier=identifier,
                    date=today,
                    defaults={'last_seen': now},
                )
            except Exception:
                # Presence recording must never break the request
                pass

            # compute current online and update peak
            window = now - datetime.timedelta(minutes=self.WINDOW_MINUTES)
            try:
                current_online = Presence.objects.filter(last_seen__gte=window).count()
                dp, _ = DailyPresence.objects.get_or_create(date=today)
                if current_online > dp.peak:
                    dp.peak = current_online
                    dp.save(update_fields=['peak'])
            except Exception:
                pass

        response = self.get_response(request)
        return response
