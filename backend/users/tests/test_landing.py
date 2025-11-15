from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from ..models import Announcement


class LandingPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_renders(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        # Basic landing content should be present
        self.assertContains(response, 'Joyland Schools')

    def test_unread_badges_reflect_announcements(self):
        # Create announcements at different times to exercise counts
        now = timezone.now()
        Announcement.objects.create(title='Old ann', message='old', is_active=True, priority=100)
        a_recent = Announcement.objects.create(title='Recent ann', message='recent', is_active=True, priority=50)
        a_very_recent = Announcement.objects.create(title='Very recent', message='very recent', is_active=True, priority=10)

        # Adjust created_at to simulate different ages
        a_recent.created_at = now - timedelta(days=10)
        a_recent.save()
        a_very_recent.created_at = now - timedelta(days=2)
        a_very_recent.save()

        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

        # Based on the landing view heuristic: teacher=all active (3),
        # student=last 7 days (1), parents=last 30 days (2)
        self.assertContains(response, '>3<', msg_prefix='Teacher unread count should be 3 somewhere in page')
        self.assertContains(response, '>1<', msg_prefix='Student unread count should be 1 somewhere in page')
        self.assertContains(response, '>2<', msg_prefix='Parents unread count should be 2 somewhere in page')
