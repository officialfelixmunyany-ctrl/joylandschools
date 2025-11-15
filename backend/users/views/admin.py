"""Administrative views for user management."""

from typing import Dict, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
import secrets
import logging

from ..models import User, StudentProfile
from ..forms import AdminCreateUserForm
from .auth import is_system_admin

logger = logging.getLogger(__name__)


@user_passes_test(is_system_admin)
def admin_create_user(request: HttpRequest) -> HttpResponse:
    """Handle manual user creation by administrators."""
    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)
        if form.is_valid():
            # Create user with random initial password
            password = secrets.token_urlsafe(8)
            user = form.save(commit=False)
            user.set_password(password)
            role = form.cleaned_data.get('role')
            user.role = role
            user.save()
            
            # Create role-specific profile if needed
            if role == 'student':
                try:
                    profile = StudentProfile.objects.create(user=user)
                    logger.info('Created student profile for user: %s', user.username)
                except Exception as e:
                    logger.error('Failed to create student profile for user: %s',
                               user.username, exc_info=e)

            # Send welcome email if requested
            if form.cleaned_data.get('send_email') and user.email:
                try:
                    subject = 'Your Joyland Schools account'
                    message = (
                        f"Hello {user.get_full_name() or user.username},\n\n"
                        f"Your account has been created.\n"
                        f"Username: {user.username}\n"
                        f"Password: {password}\n\n"
                        f"Please login and change your password."
                    )
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                    logger.info('Sent welcome email to user: %s', user.username)
                except Exception as e:
                    logger.error('Failed to send welcome email to user: %s',
                               user.username, exc_info=e)

            messages.success(request, f'User {user.username} created.')
            return redirect('admin_user_list')
    else:
        form = AdminCreateUserForm()
    return render(request, 'users/admin_create_user.html', {'form': form})


@user_passes_test(is_system_admin)
def admin_user_list(request: HttpRequest) -> HttpResponse:
    """Show list of all users."""
    users = User.objects.all()
    return render(request, 'users/admin_user_list.html', {'users': users})


@user_passes_test(is_system_admin)
def admin_user_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Handle user deletion."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        logger.info('Deleted user: %s', username)
        return redirect('admin_user_list')
    return render(request, 'users/admin_user_delete.html', {'user': user})