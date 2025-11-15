from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.core import mail
from users.admin import RegistrationRequestAdmin
from core.models import RegistrationRequest
from users.forms import RegistrationRequestForm
from users.views import create_registration_request, send_registration_emails
from unittest.mock import patch

User = get_user_model()


class RegistrationFormTests(TestCase):
    def test_form_requires_agree(self):
        data = {
            'first_name': 'Test',
            'email': 'test@example.com',
        }
        form = RegistrationRequestForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_valid(self):
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'agree': True,
            'month': 1,
            'day': 1,
            'year': 2000,
        }
        form = RegistrationRequestForm(data=data)
        self.assertTrue(form.is_valid())


class RegistrationHelpersTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'country_code': '+1',
            'phone': '555-0123',
            'month': 1,
            'day': 1,
            'year': 2000,
            'heard_friend': True,
            'agree': True
        }
    
    def test_create_registration_request(self):
        """Test helper creates registration request with correct data."""
        req = create_registration_request('student', self.valid_data)
        self.assertEqual(req.user_type, 'student')
        self.assertEqual(req.first_name, 'Test')
        self.assertEqual(req.last_name, 'User')
        self.assertEqual(req.email, 'test@example.com')
        self.assertTrue('heard_friend' in req.heard_about)
    
    def test_send_registration_emails(self):
        """Test email sending helper sends both emails."""
        req = create_registration_request('teacher', self.valid_data)
        send_registration_emails(req)
        
        self.assertEqual(len(mail.outbox), 2)
        admin_email = mail.outbox[0]
        user_email = mail.outbox[1]
        
        self.assertIn('New registration request', admin_email.subject)
        self.assertIn('teacher', admin_email.subject)
        self.assertIn('Registration received', user_email.subject)
        self.assertEqual(user_email.to[0], req.email)


class AdminApproveTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = RegistrationRequestAdmin(RegistrationRequest, self.site)
        self.factory = RequestFactory()

    @patch('django.core.mail.EmailMultiAlternatives.send')
    def test_approve_creates_user_and_sends_email(self, mock_send):
        req = RegistrationRequest.objects.create(
            user_type='student',
            first_name='Bob',
            last_name='Jones',
            email='bob.jones@example.com',
            agree=True,
        )
        request = self.factory.get('/admin/')
        # attach message storage so admin.message_user works during tests
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        queryset = RegistrationRequest.objects.filter(pk=req.pk)
        self.admin.approve_requests(request, queryset)
        user_qs = User.objects.filter(email='bob.jones@example.com')
        self.assertTrue(user_qs.exists())
        self.assertTrue(mock_send.called)

    def test_deny_action_sets_status(self):
        req = RegistrationRequest.objects.create(
            user_type='teacher',
            first_name='Denise',
            email='denise@example.com',
            agree=True,
        )
        request = self.factory.get('/admin/')
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', {})
        setattr(request, '_messages', FallbackStorage(request))
        queryset = RegistrationRequest.objects.filter(pk=req.pk)
        self.admin.deny_requests(request, queryset)
        req.refresh_from_db()
        self.assertEqual(req.status, 'denied')

    def test_duplicate_email_requests_create_multiple_entries(self):
        # system allows duplicate registration requests but admin should handle duplicates
        r1 = RegistrationRequest.objects.create(user_type='student', first_name='A', email='dup@example.com', agree=True)
        r2 = RegistrationRequest.objects.create(user_type='student', first_name='B', email='dup@example.com', agree=True)
        self.assertNotEqual(r1.pk, r2.pk)

    def test_invalid_email_fails_form(self):
        data = {'first_name': 'X', 'email': 'not-an-email', 'agree': True}
        form = RegistrationRequestForm(data=data)
        self.assertFalse(form.is_valid())
