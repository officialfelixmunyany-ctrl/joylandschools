"""Views for managing and displaying announcements."""

from typing import Dict, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import logging
from django.core.cache import cache

from core.models import Announcement, Event
from ..forms import AnnouncementForm
from .auth import is_system_admin

logger = logging.getLogger(__name__)


def _announcements_list_fragment(request: HttpRequest) -> HttpResponse:
    """Render the announcements list partial for HTMX updates."""
    announcements = Announcement.objects.get_active_for_landing()
    return render(request, 'core/includes/announcements.html', 
                 {'announcements': announcements})


def landing(request: HttpRequest) -> HttpResponse:
    """Render the landing page with announcements."""
    # Cache announcements and upcoming events for a short window to reduce DB load.
    # Keep timeout small so admins see changes quickly (30 seconds).
    announcements = cache.get('landing_announcements')
    if announcements is None:
        announcements_qs = Announcement.objects.get_active_for_landing()
        # store as list of dicts (safe for cache backends)
        announcements = list(announcements_qs.values('id', 'title', 'message', 'priority', 'created_at'))
        cache.set('landing_announcements', announcements, 30)

    upcoming_events = cache.get('landing_events')
    if upcoming_events is None:
        events_qs = Event.objects.upcoming(limit=3)
        upcoming_events = list(events_qs.values('id', 'title', 'start', 'end', 'location'))
        cache.set('landing_events', upcoming_events, 30)

    # Calculate unread counts for different user types
    now = timezone.now()
    recent_7 = now - timedelta(days=7)
    recent_30 = now - timedelta(days=30)
    
    counts: Dict[str, int] = {
        'teacher': Announcement.objects.filter(is_active=True).count(),
        'student': Announcement.objects.filter(
            is_active=True, created_at__gte=recent_7
        ).count(),
        'parents': Announcement.objects.filter(
            is_active=True, created_at__gte=recent_30
        ).count(),
    }
    
    return render(request, 'landing.html', 
                 {'announcements': announcements, 'unread_counts': counts, 'upcoming_events': upcoming_events})


def announcements_partial(request: HttpRequest) -> HttpResponse:
    """Render just the announcements section for AJAX updates."""
    announcements = Announcement.objects.get_active_for_landing()
    return render(request, 'core/includes/announcements.html', 
                 {'announcements': announcements})


@user_passes_test(is_system_admin)
def announcements_list(request: HttpRequest) -> HttpResponse:
    """Show all announcements (admin view)."""
    announcements = Announcement.objects.all().order_by('priority', '-created_at')
    return render(request, 'core/includes/announcements_list.html', 
                 {'announcements': announcements})


def announcements_archive(request: HttpRequest) -> HttpResponse:
    """Show archived (inactive) announcements."""
    announcements = Announcement.objects.get_archive_list()
    return render(request, 'core/announcements_archive.html', 
                 {'announcements': announcements})


from joyland.integrations.openai import OpenAIClient

@user_passes_test(is_system_admin)
def announcement_create(request: HttpRequest) -> HttpResponse:
    """Create a new announcement with optional AI assistance."""
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save()
            logger.info('Created announcement: %s', announcement.title)
            
            if request.headers.get('Hx-Request'):
                resp = _announcements_list_fragment(request)
                resp['HX-Trigger'] = 'announcementSaved'
                return resp
            return redirect('landing')
    else:
        # If AI draft requested
        if 'draft' in request.GET:
            topic = request.GET.get('topic', '')
            audience = request.GET.get('audience', 'all')
            points = request.GET.getlist('points', [])
            
            if topic and points:
                try:
                    ai_client = OpenAIClient()
                    draft = ai_client.draft_announcement(
                        topic=topic,
                        audience=audience,
                        key_points=points
                    )
                    # Pre-fill the form with AI draft
                    form = AnnouncementForm(initial={
                        'title': topic,
                        'message': draft,
                        'is_active': False,  # Draft starts inactive
                        'priority': 100  # Default priority
                    })
                    logger.info('Generated AI draft for announcement: %s', topic)
                except Exception as e:
                    logger.error('Failed to generate AI announcement draft', 
                               exc_info=e)
                    form = AnnouncementForm()
            else:
                form = AnnouncementForm()
        else:
            form = AnnouncementForm()
    
    action_url = reverse('announcement_create')
    return render(request, 'core/includes/announcement_form.html',
                 {'form': form, 'action_url': action_url})


@user_passes_test(is_system_admin)
def announcement_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Edit an existing announcement."""
    ann = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=ann)
        if form.is_valid():
            announcement = form.save()
            logger.info('Updated announcement: %s', announcement.title)
            
            if request.headers.get('Hx-Request'):
                resp = _announcements_list_fragment(request)
                resp['HX-Trigger'] = 'announcementSaved'
                return resp
            return redirect('landing')
    else:
        form = AnnouncementForm(instance=ann)
    
    action_url = reverse('announcement_edit', args=[ann.pk])
    return render(request, 'core/includes/announcement_form.html',
                 {'form': form, 'announcement': ann, 'action_url': action_url})


@user_passes_test(is_system_admin)
def announcement_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete an announcement."""
    ann = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        title = ann.title
        ann.delete()
        logger.info('Deleted announcement: %s', title)
        
        if request.headers.get('Hx-Request'):
            resp = _announcements_list_fragment(request)
            resp['HX-Trigger'] = 'announcementDeleted'
            return resp
        return redirect('landing')
    
    return render(request, 'core/includes/announcement_confirm_delete.html',
                 {'announcement': ann})