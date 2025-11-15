from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path
from .models import User, StudentProfile


class JoylandAdminSite(AdminSite):
    site_header = 'Joyland Schools Administration'
    site_title = 'Joyland Admin'
    index_title = 'Dashboard'

    def get_urls(self):
        urls = super().get_urls()
        # keep default urls
        return urls

    def index(self, request, extra_context=None):
        # provide simple role counts
        extra = extra_context or {}
        extra.update({
            'system_admin_count': User.objects.filter(role='system_admin').count(),
            'teacher_count': User.objects.filter(role='teacher').count(),
            'student_count': User.objects.filter(role='student').count(),
        })
        return super().index(request, extra_context=extra)


custom_admin_site = JoylandAdminSite(name='joyland_admin')
