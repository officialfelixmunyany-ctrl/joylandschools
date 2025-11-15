"""Authentication and access control views."""

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import StudentAccessForm, TeacherLoginForm
from ..models import StudentProfile, User


def is_system_admin(user: User) -> bool:
    """Check if a user is a system administrator.

    Args:
        user: The user to check

    Returns:
        True if the user is authenticated and has the system_admin role
    """
    return user.is_authenticated and user.role == "system_admin"


def redirect_by_role(user: User) -> str:
    """Get the appropriate redirect URL for a user based on their role.

    Args:
        user: The user to get a redirect for

    Returns:
        URL path to redirect the user to
    """
    role = getattr(user, "role", None)
    if role == "system_admin" or user.is_superuser:
        return reverse("admin_user_list")
    if role == "principal":
        return reverse("teacher_dashboard")
    if role == "teacher":
        return reverse("teacher_dashboard")
    if role == "parent":
        return reverse("parent_dashboard")
    if role == "student":
        return reverse("student_dashboard")
    return reverse("landing")


def teacher_login(request: HttpRequest) -> HttpResponse:
    """Handle teacher login via username/password."""
    # Backwards-compatible wrapper kept for existing callers.
    return role_login(request, role="teacher")


def role_login(request: HttpRequest, role: str = "teacher") -> HttpResponse:
    """Generic role-aware login view.

    - role='teacher' shows the teacher username/password form and a direct link
      to teacher registration when the user doesn't have portal access.
    - role='student' redirects to the student access flow (admission number).
    """
    role = (role or "teacher").lower()

    if role == "student":
        # Student access uses a different flow (admission/assessment lookup)
        # student_access already renders the student login-like form
        return redirect("student_access")

    # Default to a username/password login for other roles (teacher, parent, etc.)
    # Use TeacherLoginForm for username/password authentication
    if request.method == "POST":
        form = TeacherLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(redirect_by_role(user))
    else:
        form = TeacherLoginForm()

    # Pick registration URL based on role, fallback to generic registration selector
    try:
        register_url = reverse(f"register_{role}")
    except Exception:
        register_url = reverse("registration_select")

    context = {
        "form": form,
        "role": role,
        "register_url": register_url,
        "title": f"{role.capitalize()} Login",
    }
    return render(request, "users/login_base.html", context)


def student_access(request: HttpRequest) -> HttpResponse:
    """Handle student login via admission/assessment numbers."""
    if request.method == "POST":
        form = StudentAccessForm(request.POST)
        if form.is_valid():
            an = form.cleaned_data.get("admission_number")
            asses = form.cleaned_data.get("assessment_number")
            profile = None

            if an or asses:
                query = Q()
                if an:
                    query |= Q(admission_number__iexact=an)
                if asses:
                    query |= Q(assessment_number__iexact=asses)

                profile = StudentProfile.objects.filter(query).first()

            if profile:
                user = profile.user
                login(request, user)
                return redirect(redirect_by_role(user))
            form.add_error(None, "No matching student found")
    else:
        form = StudentAccessForm()
    return render(request, "users/student_access.html", {"form": form})


def user_logout(request: HttpRequest) -> HttpResponse:
    """Log out the current user."""
    logout(request)
    return redirect("landing")


@login_required(login_url="teacher_login")
def student_dashboard(request: HttpRequest) -> HttpResponse:
    """Display the student dashboard."""
    # Check if user is a student
    if hasattr(request.user, "role") and request.user.role != "student":
        return redirect(redirect_by_role(request.user))

    # Get student profile if it exists
    student_profile = None
    if hasattr(request.user, "studentprofile"):
        student_profile = request.user.studentprofile

    context = {"student": request.user, "profile": student_profile}
    return render(request, "users/student_dashboard.html", context)


@login_required(login_url="role_login")
def parent_dashboard(request: HttpRequest) -> HttpResponse:
    """Display the parent portal dashboard."""
    # Check if user is a parent
    if hasattr(request.user, "role") and request.user.role != "parent":
        return redirect(redirect_by_role(request.user))
    context = {}
    return render(request, "users/parent_dashboard.html", context)


def presence_live(request: HttpRequest) -> HttpResponse:
    """Display live presence statistics (users online now, today unique, peak)."""
    return render(request, "presence_live.html")


    context = {"user": request.user}
    return render(request, "users/parent_dashboard.html", context)
