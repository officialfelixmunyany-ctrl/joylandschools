# NEW: Import built-in auth views
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import teacher

urlpatterns = [
    path('', views.landing, name='landing'),
    path('live/', views.presence_live, name='presence_live'),
    # Role-aware login routes
    path('portal/login/teacher/', views.role_login, {'role': 'teacher'}, name='teacher_login'),
    path('portal/login/<str:role>/', views.role_login, name='role_login'),
    path('portal/student-access/', views.student_access, name='student_access'),
    path('portal/logout/', views.user_logout, name='user_logout'),
    path('portal/teacher/', teacher.teacher_dashboard, name='teacher_dashboard'),
    path('portal/teacher/generate-term-plan/', teacher.generate_term_plan, name='generate_term_plan'),
    path('portal/teacher/generate-assessment/', teacher.generate_assessment, name='generate_assessment'),
    path('portal/teacher/analyze-student/', teacher.analyze_student, name='analyze_student'),
    path('portal/teacher/get-differentiated-activities/', teacher.get_differentiated_activities, name='get_differentiated_activities'),
    path('portal/student/', views.student_dashboard, name='student_dashboard'),
    path('portal/parent/', views.parent_dashboard, name='parent_dashboard'),
    path('portal/admin/create-user/', views.admin_create_user, name='admin_create_user'),
    path('portal/admin/users/', views.admin_user_list, name='admin_user_list'),
    path('portal/admin/users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
    # optionally add logout route
    # HTMX/partial endpoint for announcements
    path('announcements-partial/', views.announcements_partial, name='announcements_partial'),
    path('announcements-archive/', views.announcements_archive, name='announcements_archive'),
    path('announcements-list/', views.announcements_list, name='announcements_list'),
    path('announcement/create/', views.announcement_create, name='announcement_create'),
    path('announcement/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcement/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),

    # === NEW: PASSWORD CHANGE URLS ===
    # This page will show the form to change password
    path(
        'portal/change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html', # We will create this template
            success_url = 'password_change_done' # Go here on success
        ),
        name='password_change'
    ),
    # This page will show a success message
    path(
        'portal/change-password/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html' # We will create this template
        ),
        name='password_change_done'
    ),
    # Registration selector and forms
    path('portal/register/', views.registration_select, name='registration_select'),
    path('portal/register/student/', views.register_student, name='register_student'),
    path('portal/register/teacher/', views.register_teacher, name='register_teacher'),
    path('portal/register/parent/', views.register_parent, name='register_parent'),
    path('portal/register/success/', views.register_success, name='register_success'),
    # Password reset flow (so admin can build reset links)
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    # one-time login used by admin approval emails
    path('one-time/<uidb64>/<token>/', views.one_time_login, name='one_time_login'),
]
