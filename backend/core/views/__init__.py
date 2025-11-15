"""Core views package - re-export commonly used views."""
from .announcements import (
    announcement_create,
    announcement_delete,
    announcement_edit,
    announcements_archive,
    announcements_list,
    announcements_partial,
    landing,
)

from .registration import (
    registration_select,
    register_student,
    register_teacher,
    register_parent,
    register_success,
    one_time_login,
)

__all__ = [
    # Announcement views
    'landing',
    'announcements_partial',
    'announcements_list',
    'announcements_archive',
    'announcement_create',
    'announcement_edit',
    'announcement_delete',
    # Registration views
    'registration_select',
    'register_student',
    'register_teacher',
    'register_parent',
    'register_success',
    'one_time_login',
]
