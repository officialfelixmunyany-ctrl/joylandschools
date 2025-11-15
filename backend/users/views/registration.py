"""Views for user registration and account creation."""

from typing import Dict, Any, Optional
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import logging

from core.models import RegistrationRequest
from ..models import User
from ..forms import RegistrationRequestForm

logger = logging.getLogger(__name__)


from joyland.integrations.openai import OpenAIClient

def create_registration_request(user_type: str, form_data: Dict[str, Any]) -> RegistrationRequest:
    """Create a new registration request from form data.
    
    Args:
        user_type: Type of user being registered ('student', 'teacher', 'parent')
        form_data: Cleaned form data from RegistrationRequestForm
        
    Returns:
        The created RegistrationRequest instance
    """
    # Create the basic request
    request = RegistrationRequest.objects.create(
        user_type=user_type,
        first_name=form_data.get('first_name', '').strip(),
        last_name=form_data.get('last_name', '').strip(),
        email=form_data.get('email', '').strip(),
        country_code=form_data.get('country_code', '').strip(),
        phone=form_data.get('phone', '').strip(),
        address=form_data.get('address', '').strip(),
        birth_month=form_data.get('month'),
        birth_day=form_data.get('day'),
        birth_year=form_data.get('year'),
        heard_about=','.join(k for k in ['heard_friend', 'heard_google', 'heard_other'] 
                           if form_data.get(k)),
        agree=bool(form_data.get('agree')),
    )
    
    # For student registrations, get AI analysis
    if user_type == 'student':
        try:
            ai_client = OpenAIClient()
            analysis = ai_client.analyze_student_application(form_data)
            
            # Store AI insights in notes field
            insights = [
                f"AI Analysis Results:",
                f"Recommended Level: {analysis['recommended_class_level']}",
                f"Learning Style: {analysis['learning_style']}",
                "",
                "Academic Interests:",
                *[f"- {interest}" for interest in analysis['academic_interests']],
                "",
                "Support Considerations:",
                *[f"- {need}" for need in analysis['support_needs']]
            ]
            request.notes = "\n".join(insights)
            request.save()
            
            logger.info(
                'Added AI analysis to student registration request ID=%s', 
                request.id
            )
        except Exception as e:
            logger.error(
                'Failed to generate AI analysis for student registration ID=%s',
                request.id,
                exc_info=e
            )
    
    return request


def send_registration_emails(request: RegistrationRequest, admin_email: Optional[str] = None) -> None:
    """Send confirmation emails for a registration request.
    
    Sends two emails:
    1. To admin notifying of new request
    2. To applicant confirming receipt
    
    Args:
        request: The registration request that was created
        admin_email: Optional override for admin notification address
    """
    if not admin_email:
        admin_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        subject = f"New registration request: {request.get_user_type_display()}"
        msg = f"A new registration request was submitted:\n\n{request}\n\nReview in admin."
        send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [admin_email])
        send_mail('Registration received', 
                 'Thanks — we received your application.', 
                 settings.DEFAULT_FROM_EMAIL, 
                 [request.email])
        logger.info('Sent registration emails for request ID=%s', request.id)
    except Exception as e:
        logger.error('Failed to send registration emails for request ID=%s', 
                    request.id, exc_info=e)


def get_date_choices() -> Dict[str, list]:
    """Get standard date dropdown choices for registration forms."""
    return {
        'months': list(range(1, 13)),
        'days': list(range(1, 32)),
        'years': list(range(2006, 1940, -1))
    }


def registration_select(request: HttpRequest) -> HttpResponse:
    """Show the registration type selection page."""
    return render(request, 'users/registration_select.html')


def register_student(request: HttpRequest) -> HttpResponse:
    """Handle student registration requests."""
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            req = create_registration_request('student', form.cleaned_data)
            send_registration_emails(req)
            return redirect('register_success')
    else:
        form = RegistrationRequestForm()
    
    return render(request, 'users/register_student.html', 
                 {'form': form, **get_date_choices()})


def register_teacher(request: HttpRequest) -> HttpResponse:
    """Handle teacher registration requests."""
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            req = create_registration_request('teacher', form.cleaned_data)
            send_registration_emails(req)
            return redirect('register_success')
    else:
        form = RegistrationRequestForm()
    
    return render(request, 'users/register_teacher.html',
                 {'form': form, **get_date_choices()})


def register_parent(request: HttpRequest) -> HttpResponse:
    """Handle parent registration requests."""
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            req = create_registration_request('parent', form.cleaned_data)
            send_registration_emails(req)
            return redirect('register_success')
    else:
        form = RegistrationRequestForm()
    
    return render(request, 'users/register_parent.html',
                 {'form': form, **get_date_choices()})


def register_success(request: HttpRequest) -> HttpResponse:
    """Show registration success page."""
    return render(request, 'users/register_success.html')


def one_time_login(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """Handle one-time login links sent on registration approval.
    
    If token is valid:
    1. Log the user in
    2. Redirect to password change page
    
    Args:
        uidb64: Base64-encoded user ID
        token: One-time login token
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception as e:
        logger.error('Failed to decode one-time login token', exc_info=e)
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        logger.info('One-time login successful for user: %s', user.username)
        return redirect('password_change')
    
    messages.error(request, 'Invalid or expired link')
    return redirect('landing')