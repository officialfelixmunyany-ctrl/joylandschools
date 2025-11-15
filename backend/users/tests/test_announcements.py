from django.test import TestCase
from django.urls import reverse
from ..models import Announcement
from ..models import User


class AnnouncementsTests(TestCase):
    def test_announcements_list_and_partial(self):
        # empty list
        resp = self.client.get(reverse('announcements_partial'))
        self.assertEqual(resp.status_code, 200)

        # create an announcement
        a = Announcement.objects.create(title='Test', message='Hello', is_active=True, priority=10)
        resp2 = self.client.get(reverse('announcements_partial'))
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, 'Test')

        # partial
        resp3 = self.client.get(reverse('announcements_partial'))
        self.assertEqual(resp3.status_code, 200)
        self.assertContains(resp3, 'Test')

    def test_create_edit_delete_via_views(self):
        # login as superuser to perform admin actions
        User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        self.client.login(username='admin', password='pass')

        # create via POST
        resp = self.client.post(reverse('announcement_create'), {'title': 'C1', 'message': 'X', 'is_active': True, 'priority': 5})
        self.assertEqual(Announcement.objects.count(), 1)
        a = Announcement.objects.first()
        # edit
        resp2 = self.client.post(reverse('announcement_edit', args=[a.pk]), {'title': 'C1-up', 'message': 'Y', 'is_active': True, 'priority': 5})
        a.refresh_from_db()
        self.assertEqual(a.title, 'C1-up')
        # delete
        resp3 = self.client.post(reverse('announcement_delete', args=[a.pk]))
        self.assertEqual(Announcement.objects.count(), 0)

    def test_anonymous_cannot_see_admin_buttons(self):
        # landing page should not show New/Edit/Delete buttons to anonymous users
        resp = self.client.get(reverse('landing'))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, 'New')
