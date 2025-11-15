"""Core registration views (moved from users.views.registration)."""
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
from users.models import User
from users.forms import RegistrationRequestForm

logger = logging.getLogger(__name__)


from joyland.integrations.openai import OpenAIClient


def create_registration_request(user_type: str, form_data: Dict[str, Any]) -> RegistrationRequest:
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
        heard_about=','.join(k for k in ['heard_friend', 'heard_google', 'heard_other'] if form_data.get(k)),
        agree=bool(form_data.get('agree')),
    )

    if user_type == 'student':
        try:
            ai_client = OpenAIClient()
            analysis = ai_client.analyze_student_application(form_data)
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
            logger.info('Added AI analysis to student registration request ID=%s', request.id)
        except Exception as e:
            logger.error('Failed to generate AI analysis for student registration ID=%s', request.id, exc_info=e)

    return request


def send_registration_emails(request: RegistrationRequest, admin_email: Optional[str] = None) -> None:
    if not admin_email:
        admin_email = settings.DEFAULT_FROM_EMAIL
    try:
        subject = f"New registration request: {request.get_user_type_display()}"
        msg = f"A new registration request was submitted:\n\n{request}\n\nReview in admin."
        send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [admin_email])
        send_mail('Registration received', 'Thanks — we received your application.', settings.DEFAULT_FROM_EMAIL, [request.email])
        logger.info('Sent registration emails for request ID=%s', request.id)
    except Exception as e:
        logger.error('Failed to send registration emails for request ID=%s', request.id, exc_info=e)


def get_date_choices():
    return {
        'months': list(range(1, 13)),
        'days': list(range(1, 32)),
        'years': list(range(2006, 1940, -1))
    }


def registration_select(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/registration_select.html')


def register_student(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            req = create_registration_request('student', form.cleaned_data)
            send_registration_emails(req)
            return redirect('register_success')
    else:
        form = RegistrationRequestForm()
    return render(request, 'users/register_student.html', {'form': form, **get_date_choices()})


def register_teacher(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            req = create_registration_request('teacher', form.cleaned_data)
            send_registration_emails(req)
            return redirect('register_success')
    else:
        form = RegistrationRequestForm()
    return render(request, 'users/register_teacher.html', {'form': form, **get_date_choices()})


def register_parent(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            req = create_registration_request('parent', form.cleaned_data)
            send_registration_emails(req)
            return redirect('register_success')
    else:
        form = RegistrationRequestForm()
    return render(request, 'users/register_parent.html', {'form': form, **get_date_choices()})


def register_success(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/register_success.html')


def one_time_login(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
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
