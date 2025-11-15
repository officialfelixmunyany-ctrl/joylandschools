"""Views package for user management."""

from .admin import (
    admin_create_user,
    admin_user_delete,
    admin_user_list,
)
from core.views import (
    announcement_create,
    announcement_delete,
    announcement_edit,
    announcements_archive,
    announcements_list,
    announcements_partial,
    landing,
)
from .auth import (
    is_system_admin,
    parent_dashboard,
    presence_live,
    redirect_by_role,
    role_login,
    student_access,
    student_dashboard,
    teacher_login,
    user_logout,
)
from core.views import (
    one_time_login,
    register_parent,
    register_student,
    register_success,
    register_teacher,
    registration_select,
)

__all__ = [
    # Auth views
    "teacher_login",
    "student_access",
    "user_logout",
    "redirect_by_role",
    "is_system_admin",
    "student_dashboard",
    "role_login",
    "parent_dashboard",
    "presence_live",
    # Announcement views
    "landing",
    "announcements_partial",
    "announcements_list",
    "announcements_archive",
    "announcement_create",
    "announcement_edit",
    "announcement_delete",
    # Registration views
    "registration_select",
    "register_student",
    "register_teacher",
    "register_parent",
    "register_success",
    "one_time_login",
    # Admin views
    "admin_create_user",
    "admin_user_list",
    "admin_user_delete",
]
