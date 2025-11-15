"""Unit tests for teacher views."""

from django.test import TestCase, Client
from django.urls import reverse
import json
from unittest.mock import patch, MagicMock
from ..models import User
from joyland.integrations.education import EducationalAIService


class TeacherViewsTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create a teacher user
        self.teacher = User.objects.create_user(
            username='testteacher',
            email='teacher@joyland.edu',
            password='testpass123',
            role='teacher'
        )
        
        # Create a non-teacher user
        self.student = User.objects.create_user(
            username='teststudent',
            email='student@joyland.edu',
            password='testpass123',
            role='student'
        )
        
        # Common test data
        self.test_subject = 'Mathematics'
        self.test_grade = '9th'
        self.test_term = 2
        self.test_objective = 'Understand and apply quadratic equations'

    def test_teacher_dashboard_access(self):
        """Test teacher dashboard access permissions."""
        # Test unauthenticated access
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test student access
        self.client.force_login(self.student)
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test teacher access
        self.client.force_login(self.teacher)
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/teacher_dashboard.html')

    @patch.object(EducationalAIService, 'generate_term_plan')
    def test_generate_term_plan(self, mock_generate):
        """Test term plan generation endpoint."""
        # Set up mock return value
        mock_generate.return_value = [
            MagicMock(
                description='Master quadratic equations',
                skills=['solving equations', 'graphing'],
                assessment_criteria=['Can solve basic equations']
            )
        ]
        
        # Test without authentication
        response = self.client.post(
            reverse('generate_term_plan'),
            data=json.dumps({
                'subject': self.test_subject,
                'grade_level': self.test_grade,
                'term': self.test_term
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)
        
        # Test with teacher authentication
        self.client.force_login(self.teacher)
        response = self.client.post(
            reverse('generate_term_plan'),
            data=json.dumps({
                'subject': self.test_subject,
                'grade_level': self.test_grade,
                'term': self.test_term
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('objectives', data)
        mock_generate.assert_called_once()

    @patch.object(EducationalAIService, 'generate_assessment')
    def test_generate_assessment(self, mock_generate):
        """Test assessment generation endpoint."""
        # Set up mock return value
        mock_generate.return_value = [
            MagicMock(
                question='Solve x²+2x+1=0',
                rubric='5 points for correct solution',
                sample_answer='x=-1',
                max_score=5
            )
        ]
        
        # Test with teacher authentication
        self.client.force_login(self.teacher)
        response = self.client.post(
            reverse('generate_assessment'),
            data=json.dumps({
                'objective': self.test_objective,
                'type': 'formative',
                'level': 'standard'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('assessment_items', data)
        mock_generate.assert_called_once()

    @patch.object(EducationalAIService, 'analyze_student_progress')
    def test_analyze_student(self, mock_analyze):
        """Test student analysis endpoint."""
        # Set up mock return value
        mock_analyze.return_value = MagicMock(
            objectives_mastered=['Quadratic Equations'],
            areas_for_growth=['Complex Numbers'],
            recommendations=['More practice with imaginary numbers']
        )
        
        # Test with teacher authentication
        self.client.force_login(self.teacher)
        response = self.client.post(
            reverse('analyze_student'),
            data=json.dumps({
                'student_id': '12345',
                'subject': self.test_subject
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('mastered', data)
        self.assertIn('growth_areas', data)
        self.assertIn('recommendations', data)
        mock_analyze.assert_called_once()

    @patch.object(EducationalAIService, 'generate_differentiated_activities')
    def test_get_differentiated_activities(self, mock_generate):
        """Test differentiated activities generation endpoint."""
        # Set up mock return value
        mock_generate.return_value = [
            {
                'level': 'support',
                'description': 'Guided practice with basic equations',
                'materials': ['Worksheet', 'Calculator'],
                'duration': 30
            }
        ]
        
        # Test with teacher authentication
        self.client.force_login(self.teacher)
        response = self.client.post(
            reverse('get_differentiated_activities'),
            data=json.dumps({
                'objective': self.test_objective,
                'class_id': 'math-9a'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('activities', data)
        mock_generate.assert_called_once()

    def test_missing_required_fields(self):
        """Test handling of missing required fields."""
        self.client.force_login(self.teacher)
        
        # Test term plan generation with missing fields
        response = self.client.post(
            reverse('generate_term_plan'),
            data=json.dumps({'subject': self.test_subject}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test assessment generation with missing fields
        response = self.client.post(
            reverse('generate_assessment'),
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test student analysis with missing fields
        response = self.client.post(
            reverse('analyze_student'),
            data=json.dumps({'student_id': '12345'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test activities generation with missing fields
        response = self.client.post(
            reverse('get_differentiated_activities'),
            data=json.dumps({'objective': self.test_objective}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    @patch.object(EducationalAIService, 'generate_term_plan')
    def test_error_handling(self, mock_generate):
        """Test error handling in views."""
        # Simulate an error in the AI service
        mock_generate.side_effect = Exception('AI service error')
        
        self.client.force_login(self.teacher)
        response = self.client.post(
            reverse('generate_term_plan'),
            data=json.dumps({
                'subject': self.test_subject,
                'grade_level': self.test_grade,
                'term': self.test_term
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertIn('error', data)