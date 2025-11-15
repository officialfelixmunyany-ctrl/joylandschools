from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging
from django.db.models import Q
from .forms import TeacherLoginForm, StudentAccessForm, AdminCreateUserForm, AnnouncementForm, RegistrationRequestForm

logger = logging.getLogger(__name__)

def create_registration_request(user_type, form_data):
    """Create a RegistrationRequest from form data."""
    return RegistrationRequest.objects.create(
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

def send_registration_emails(request, admin_email=None):
    """Send registration confirmation emails to admin and applicant."""
    if not admin_email:
        admin_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        subject = f"New registration request: {request.get_user_type_display()}"
        msg = f"A new registration request was submitted:\\n\\n{request}\\n\\nReview in admin."
        send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [admin_email])
        send_mail('Registration received', 'Thanks — we received your application.', 
                 settings.DEFAULT_FROM_EMAIL, [request.email])
        logger.info('Sent registration emails for request ID=%s', request.id)
    except Exception as e:
        logger.error('Failed to send registration emails for request ID=%s', 
                    request.id, exc_info=e)
        # We don't re-raise as this shouldn't block the user flow, but we do log it

# === IMPORTS MOVED TO TOP ===
from .forms import TeacherLoginForm, StudentAccessForm, AdminCreateUserForm, AnnouncementForm
from .models import User, StudentProfile
from core.models import Announcement, RegistrationRequest
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import secrets


def redirect_by_role(user):
    role = getattr(user, 'role', None)
    if role == 'system_admin' or user.is_superuser:
        return reverse('admin_user_list')
    if role == 'principal':
        return reverse('teacher_dashboard')
    if role == 'teacher':
        return reverse('teacher_dashboard')
    if role == 'student':
        return reverse('student_dashboard')
    return reverse('landing')


def landing(request):
    # CLEANED: Use the manager method from models.py
    announcements = Announcement.objects.get_active_for_landing()

    # Unread counts logic (unchanged)
    now = timezone.now()
    recent_7 = now - timedelta(days=7)
    recent_30 = now - timedelta(days=30)
    
    teacher_unread = Announcement.objects.filter(is_active=True).count()
    student_unread = Announcement.objects.filter(is_active=True, created_at__gte=recent_7).count()
    parents_unread = Announcement.objects.filter(is_active=True, created_at__gte=recent_30).count()

    unread_counts = {
        'teacher': teacher_unread,
        'student': student_unread,
        'parents': parents_unread,
    }
    return render(request, 'landing.html', {'announcements': announcements, 'unread_counts': unread_counts})


def announcements_partial(request):
    # CLEANED: Use the manager method
    announcements = Announcement.objects.get_active_for_landing()
    return render(request, 'core/includes/announcements.html', {'announcements': announcements})


def _announcements_list_fragment(request):
    # CLEANED: Use the manager method
    announcements = Announcement.objects.get_active_for_landing()
    content = render(request, 'core/includes/announcements.html', {'announcements': announcements})
    return content


def is_system_admin(user):
    return user.is_authenticated and user.role == 'system_admin'


@user_passes_test(is_system_admin)
def announcements_list(request):
    announcements = Announcement.objects.all().order_by('priority', '-created_at')
    return render(request, 'core/includes/announcements_list.html', {'announcements': announcements})


def announcements_archive(request):
    # CLEANED: Use the manager method
    announcements = Announcement.objects.get_archive_list()
    return render(request, 'core/announcements_archive.html', {'announcements': announcements})


@user_passes_test(is_system_admin)
def announcement_create(request):
    # (Imports were removed from here)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('Hx-Request'):
                resp = _announcements_list_fragment(request)
                resp['HX-Trigger'] = 'announcementSaved'
                return resp
            return redirect('landing')
    else:
        form = AnnouncementForm()
    action_url = reverse('announcement_create')
    return render(request, 'core/includes/announcement_form.html', {'form': form, 'action_url': action_url})


@user_passes_test(is_system_admin)
def announcement_edit(request, pk):
    # (Imports were removed from here)
    ann = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=ann)
        if form.is_valid():
            form.save()
            if request.headers.get('Hx-Request'):
                resp = _announcements_list_fragment(request)
                resp['HX-Trigger'] = 'announcementSaved'
                return resp
            return redirect('landing')
    else:
        form = AnnouncementForm(instance=ann)
    action_url = reverse('announcement_edit', args=[ann.pk])
    return render(request, 'core/includes/announcement_form.html', {'form': form, 'announcement': ann, 'action_url': action_url})


@user_passes_test(is_system_admin)
def announcement_delete(request, pk):
    # (Imports were removed from here)
    ann = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        ann.delete()
        if request.headers.get('Hx-Request'):
            resp = _announcements_list_fragment(request)
            resp['HX-Trigger'] = 'announcementDeleted'
            return resp
        return redirect('landing')
    return render(request, 'core/includes/announcement_confirm_delete.html', {'announcement': ann})


def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # redirect based on role
            return redirect(redirect_by_role(user))
    else:
        form = TeacherLoginForm()
    return render(request, 'users/teacher_login.html', {'form': form})


def student_access(request):
    if request.method == 'POST':
        form = StudentAccessForm(request.POST)
        if form.is_valid():
            an = form.cleaned_data.get('admission_number')
            asses = form.cleaned_data.get('assessment_number')
            profile = None

            # === FASTER SEARCH: Use Q objects for a single query ===
            if an or asses:
                query = Q()
                if an:
                    query |= Q(admission_number__iexact=an)
                if asses:
                    query |= Q(assessment_number__iexact=asses)

                profile = StudentProfile.objects.filter(query).first()
            # === END FASTER SEARCH ===

            if profile:
                user = profile.user
                login(request, user)
                return redirect(redirect_by_role(user))
            form.add_error(None, 'No matching student found')
    else:
        form = StudentAccessForm()
    return render(request, 'users/student_access.html', {'form': form})


@login_required
def teacher_dashboard(request):
    return render(request, 'users/teacher_dashboard.html')


@login_required
def student_dashboard(request):
    return render(request, 'users/student_dashboard.html')


@user_passes_test(is_system_admin)
def admin_create_user(request):
    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)
        if form.is_valid():
            # create user but set a random password
            password = secrets.token_urlsafe(8)
            user = form.save(commit=False)
            user.set_password(password)
            role = form.cleaned_data.get('role')
            user.role = role
            user.save()
            if role == 'student':
                StudentProfile.objects.create(user=user)

            # send email if requested (console backend in settings)
            if form.cleaned_data.get('send_email') and user.email:
                subject = 'Your Joyland Schools account'
                message = f"Hello {user.get_full_name() or user.username},\n\nYour account has been created.\nUsername: {user.username}\nPassword: {password}\n\nPlease login and change your password."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            messages.success(request, f'User {user.username} created.')
            return redirect('admin_user_list')
    else:
        form = AdminCreateUserForm()
    return render(request, 'users/admin_create_user.html', {'form': form})


@user_passes_test(is_system_admin)
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'users/admin_user_list.html', {'users': users})


@user_passes_test(is_system_admin)
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_user_list')
    return render(request, 'users/admin_user_delete.html', {'user': user})


def user_logout(request):
    logout(request)
    return redirect('landing')


def registration_select(request):
    return render(request, 'users/registration_select.html')


def get_date_choices():
    """Return standard date choices for registration forms."""
    return {
        'months': list(range(1, 13)),
        'days': list(range(1, 32)),
        'years': list(range(2006, 1940, -1))
    }

def register_student(request):
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


def register_teacher(request):
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


def register_parent(request):
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


def register_success(request):
    return render(request, 'users/register_success.html')


def one_time_login(request, uidb64, token):
    """Allow a user to sign in via a one-time link sent on approval.
    If token is valid, log the user in and redirect to password change page.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # log the user in and redirect to change-password flow
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('password_change')
    messages.error(request, 'Invalid or expired link')
    return redirect('landing')
