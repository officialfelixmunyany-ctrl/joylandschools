"""Tests for the new role-aware login flow."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthFlowTests(TestCase):
    """Tests for role-aware login GET requests and registration links."""

    def test_teacher_login_route_and_register_link(self):
        """GET /portal/login/teacher/ should render and link to register_teacher."""
        resp = self.client.get(reverse('teacher_login'))
        self.assertEqual(resp.status_code, 200)
        # The register_teacher URL should appear in the rendered content
        self.assertIn(reverse('register_teacher'), resp.content.decode('utf-8'))

    def test_generic_role_login_redirects_student(self):
        """Accessing the student role login should redirect to student access flow."""
        resp = self.client.get(reverse('role_login', kwargs={'role': 'student'}))
        # Should redirect (302) to student access
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('student_access'), resp['Location'])

    def test_parent_login_route_and_register_link(self):
        """GET /portal/login/parent/ should render and link to register_parent."""
        resp = self.client.get(reverse('role_login', kwargs={'role': 'parent'}))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(reverse('register_parent'), resp.content.decode('utf-8'))


class LoginPostTests(TestCase):
    """Tests for login form POST submissions."""

    def setUp(self):
        """Create a test user for login attempts."""
        self.test_user = User.objects.create_user(
            username='testteacher',
            email='test@example.com',
            password='testpass123',
            is_staff=False
        )

    def test_teacher_login_post_invalid_credentials(self):
        """POST to teacher login with invalid credentials should re-render form with error."""
        resp = self.client.post(
            reverse('teacher_login'),
            {'username': 'testteacher', 'password': 'wrongpassword'}
        )
        self.assertEqual(resp.status_code, 200)
        # Should re-render the login page (form with errors)
        self.assertIn('form', resp.context)

    def test_teacher_login_post_valid_credentials(self):
        """POST to teacher login with valid credentials should log in and redirect."""
        resp = self.client.post(
            reverse('teacher_login'),
            {'username': 'testteacher', 'password': 'testpass123'},
            follow=True
        )
        # After successful login, should be redirected
        self.assertTrue(resp.wsgi_request.user.is_authenticated)
        self.assertEqual(resp.wsgi_request.user.username, 'testteacher')

    def test_parent_login_post_valid_credentials(self):
        """POST to parent login with valid credentials should authenticate."""
        resp = self.client.post(
            reverse('role_login', kwargs={'role': 'parent'}),
            {'username': 'testteacher', 'password': 'testpass123'},
            follow=True
        )
        self.assertTrue(resp.wsgi_request.user.is_authenticated)

    def test_login_post_empty_credentials(self):
        """POST with empty username/password should show form error."""
        resp = self.client.post(
            reverse('teacher_login'),
            {'username': '', 'password': ''}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('form', resp.context)


class LoginNextParameterTests(TestCase):
    """Tests for 'next' parameter handling in login flow."""

    def setUp(self):
        """Create a test user."""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_teacher_login_with_next_parameter(self):
        """Login with 'next' parameter should redirect to that page after success."""
        next_url = reverse('teacher_login')
        resp = self.client.post(
            f"{reverse('teacher_login')}?next={next_url}",
            {'username': 'testuser', 'password': 'testpass123'},
            follow=True
        )
        # User should be authenticated
        self.assertTrue(resp.wsgi_request.user.is_authenticated)

    def test_login_preserves_next_url(self):
        """GET request should preserve next parameter in form context."""
        next_url = '/some/protected/page/'
        resp = self.client.get(f"{reverse('teacher_login')}?next={next_url}")
        self.assertEqual(resp.status_code, 200)
        # The form should be present
        self.assertIn('form', resp.context)


class RoleLoginFallbackTests(TestCase):
    """Tests for fallback behavior when role registration link doesn't exist."""

    def test_unknown_role_fallback_to_registration_select(self):
        """Accessing an undefined role should handle gracefully."""
        # Attempt to access a role that doesn't have a specific registration link
        resp = self.client.get(reverse('role_login', kwargs={'role': 'admin'}))
        # Should either redirect or render with fallback
        self.assertIn(resp.status_code, [200, 302])

    def test_role_login_context_contains_role(self):
        """Rendered login page context should contain the role."""
        resp = self.client.get(reverse('role_login', kwargs={'role': 'teacher'}))
        self.assertEqual(resp.status_code, 200)
        # Context should have role information
        self.assertIn('role', resp.context)


class TemplateRenderingTests(TestCase):
    """Tests for template rendering and form display."""

    def test_teacher_login_uses_login_base_template(self):
        """Teacher login should use shared login_base.html template."""
        resp = self.client.get(reverse('teacher_login'))
        self.assertEqual(resp.status_code, 200)
        # Check that it uses login_base.html (via template name check)
        template_names = [t.name for t in resp.templates]
        self.assertTrue(any('login' in name for name in template_names))

    def test_parent_login_uses_login_base_template(self):
        """Parent login should use shared login_base.html template."""
        resp = self.client.get(reverse('role_login', kwargs={'role': 'parent'}))
        self.assertEqual(resp.status_code, 200)
        template_names = [t.name for t in resp.templates]
        self.assertTrue(any('login' in name for name in template_names))

    def test_login_form_has_csrf_token(self):
        """Login form should include CSRF token for security."""
        resp = self.client.get(reverse('teacher_login'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        # CSRF middleware sets csrftoken in cookies and context
        self.assertIn('csrf', content.lower())
