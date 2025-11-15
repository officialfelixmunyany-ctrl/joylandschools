"""Teacher dashboard with AI-powered planning tools."""

from typing import Dict, Any, List
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
import json
import logging

from joyland.integrations.education import EducationalAIService
from joyland.integrations.openai import OpenAIClient
from joyland.cache_utils import AIOperationCache
from ..models import User

logger = logging.getLogger(__name__)


def is_teacher(user: User) -> bool:
    """Check if user is a teacher or admin."""
    return user.is_authenticated and user.role in ('teacher', 'system_admin')


@user_passes_test(is_teacher)
def teacher_dashboard(request: HttpRequest) -> HttpResponse:
    """Render the teacher dashboard with planning tools."""
    return render(request, 'users/teacher_dashboard.html', {
        'subjects': get_teacher_subjects(request.user),
        'current_term': get_current_term(),
        'class_profiles': get_class_profiles(request.user)
    })


@user_passes_test(is_teacher)
@require_http_methods(['POST'])
def generate_term_plan(request: HttpRequest) -> JsonResponse:
    """Generate a term plan using AI."""
    try:
        data = json.loads(request.body)
        subject = data.get('subject')
        grade_level = data.get('grade_level')
        term = data.get('term')
        
        if not all([subject, grade_level, term]):
            return JsonResponse(
                {'error': 'Missing required fields'}, 
                status=400
            )
        
        # Check cache first
        cached = AIOperationCache.get_cached_term_plan(
            teacher_id=request.user.id,
            subject=subject,
            grade=grade_level,
            term=term
        )
        if cached:
            logger.debug(f"Returning cached term plan for {subject} {grade_level}")
            return JsonResponse({'objectives': cached, 'cached': True})
        
        ai_service = EducationalAIService(OpenAIClient())
        objectives = ai_service.generate_term_plan(
            subject=subject,
            grade_level=grade_level,
            term=term,
            existing_objectives=get_previous_objectives(request.user, subject, grade_level)
        )
        
        result = [
            {
                'description': obj.description,
                'skills': obj.skills,
                'assessment_criteria': obj.assessment_criteria
            }
            for obj in objectives
        ]
        
        # Cache the result
        AIOperationCache.cache_term_plan(
            teacher_id=request.user.id,
            subject=subject,
            grade=grade_level,
            term=term,
            plan_data=result
        )
        
        return JsonResponse({
            'objectives': result,
            'cached': False
        })
    except Exception as e:
        logger.error('Failed to generate term plan', exc_info=e)
        return JsonResponse(
            {'error': 'Failed to generate plan'}, 
            status=500
        )


@user_passes_test(is_teacher)
@require_http_methods(['POST'])
def generate_assessment(request: HttpRequest) -> JsonResponse:
    """Generate an assessment for a learning objective."""
    try:
        data = json.loads(request.body)
        objective = data.get('objective')
        assessment_type = data.get('type', 'formative')
        student_level = data.get('level', 'standard')
        
        if not objective:
            return JsonResponse(
                {'error': 'Missing learning objective'}, 
                status=400
            )
        
        # Check cache first
        cached = AIOperationCache.get_cached_assessment(
            teacher_id=request.user.id,
            objective=objective,
            assessment_type=assessment_type,
            level=student_level
        )
        if cached:
            logger.debug(f"Returning cached assessment for objective")
            return JsonResponse({'assessment_items': cached, 'cached': True})
        
        ai_service = EducationalAIService(OpenAIClient())
        items = ai_service.generate_assessment(
            objective=objective,
            assessment_type=assessment_type,
            student_level=student_level
        )
        
        result = [
            {
                'question': item.question,
                'rubric': item.rubric,
                'sample_answer': item.sample_answer,
                'max_score': item.max_score
            }
            for item in items
        ]
        
        # Cache the result
        AIOperationCache.cache_assessment(
            teacher_id=request.user.id,
            objective=objective,
            assessment_type=assessment_type,
            level=student_level,
            assessment_data=result
        )
        
        return JsonResponse({
            'assessment_items': result,
            'cached': False
        })
    except Exception as e:
        logger.error('Failed to generate assessment', exc_info=e)
        return JsonResponse(
            {'error': 'Failed to generate assessment'}, 
            status=500
        )


@user_passes_test(is_teacher)
@require_http_methods(['POST'])
def analyze_student(request: HttpRequest) -> JsonResponse:
    """Analyze a student's progress using AI."""
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        subject = data.get('subject')
        
        if not all([student_id, subject]):
            return JsonResponse(
                {'error': 'Missing required fields'}, 
                status=400
            )
        
        # Get student data from your actual database
        student_data = get_student_data(student_id, subject)
        
        ai_service = EducationalAIService(OpenAIClient())
        progress = ai_service.analyze_student_progress(
            student_data=student_data,
            subject_area=subject
        )
        
        return JsonResponse({
            'mastered': progress.objectives_mastered,
            'growth_areas': progress.areas_for_growth,
            'recommendations': progress.recommendations
        })
    except Exception as e:
        logger.error('Failed to analyze student progress', exc_info=e)
        return JsonResponse(
            {'error': 'Failed to analyze progress'}, 
            status=500
        )


@user_passes_test(is_teacher)
@require_http_methods(['POST'])
def get_differentiated_activities(request: HttpRequest) -> JsonResponse:
    """Get differentiated activities for a learning objective."""
    try:
        data = json.loads(request.body)
        objective = data.get('objective')
        class_id = data.get('class_id')
        
        if not all([objective, class_id]):
            return JsonResponse(
                {'error': 'Missing required fields'}, 
                status=400
            )
        
        # Get actual class profile from your database
        class_profile = get_class_profile(class_id)
        
        ai_service = EducationalAIService(OpenAIClient())
        activities = ai_service.generate_differentiated_activities(
            objective=objective,
            class_profile=class_profile
        )
        
        return JsonResponse({'activities': activities})
    except Exception as e:
        logger.error('Failed to generate activities', exc_info=e)
        return JsonResponse(
            {'error': 'Failed to generate activities'}, 
            status=500
        )


# Helper functions that would connect to your actual database
def get_teacher_subjects(user: User) -> Dict[str, list]:
    """Get subjects taught by teacher."""
    # This would query your actual teaching assignments
    return {
        'Mathematics': ['9th', '10th'],
        'Physics': ['10th']
    }


def get_current_term() -> int:
    """Get the current academic term."""
    # This would use your actual academic calendar
    return 2  # Example: Term 2


def get_class_profiles(user: User) -> Dict[str, Dict[str, int]]:
    """Get student level distributions for teacher's classes."""
    # This would query your actual class rosters
    return {
        'Mathematics 9A': {
            'support': 5,
            'standard': 15,
            'extension': 5
        },
        'Physics 10B': {
            'support': 3,
            'standard': 20,
            'extension': 7
        }
    }


def get_previous_objectives(
    user: User,
    subject: str,
    grade: str
) -> List[str]:
    """Get previously covered learning objectives."""
    # This would query your curriculum tracking system
    return [
        "Understand linear equations",
        "Graph quadratic functions",
        "Solve systems of equations"
    ]


def get_student_data(
    student_id: str,
    subject: str
) -> Dict[str, Any]:
    """Get student's academic data."""
    # This would query your student records system
    return {
        'student_id': student_id,
        'assessments': [
            {
                'date': '2025-10-01',
                'topic': 'Quadratic Functions',
                'score': 85,
                'max': 100,
                'notes': 'Strong understanding of graphing'
            },
            {
                'date': '2025-10-15',
                'topic': 'Polynomial Division',
                'score': 75,
                'max': 100,
                'notes': 'Needs practice with remainder theorem'
            }
        ],
        'teacher_notes': 'Shows good analytical skills, needs support with algebraic proofs'
    }


def get_class_profile(class_id: str) -> Dict[str, int]:
    """Get student level distribution for a class."""
    # This would query your class roster system
    return {
        'support': 4,
        'standard': 18,
        'extension': 6
    }