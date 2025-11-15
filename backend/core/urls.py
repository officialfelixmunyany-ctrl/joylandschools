from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('announcements/partial/', views.announcements_partial, name='announcements_partial'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('announcements/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    path('announcements/archive/', views.announcements_archive, name='announcements_archive'),
    # Registration flows
    path('register/select/', views.registration_select, name='registration_select'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('register/parent/', views.register_parent, name='register_parent'),
    path('register/success/', views.register_success, name='register_success'),
    path('one-time-login/<str:uidb64>/<str:token>/', views.one_time_login, name='one_time_login'),
]
