from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import User, StudentProfile, StaffProfile, PrincipalProfile
from .admin_site import custom_admin_site


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admission_number', 'assessment_number')

    def admission_badge(self, obj):
        return format_html('<span class="badge bg-secondary">{}</span>', obj.admission_number)


# Also register the models with the custom admin site
custom_admin_site.register(StudentProfile, StudentProfileAdmin)


class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'email', 'is_active', 'workload_status')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    actions = ['analyze_workload']
    
    def workload_status(self, obj):
        """Display workload status with color coding."""
        hours = self._get_teaching_hours(obj)
        if hours > 25:
            return format_html(
                '<span style="color: red;">Heavy ({} hrs/week)</span>', 
                hours
            )
        elif hours > 20:
            return format_html(
                '<span style="color: orange;">Moderate ({} hrs/week)</span>', 
                hours
            )
        return format_html(
            '<span style="color: green;">Light ({} hrs/week)</span>', 
            hours
            )
    workload_status.short_description = 'Teaching Load'
    
    def _get_teaching_hours(self, obj):
        """Get total teaching hours for a staff member."""
        # This would normally query your assignments model
        # For demo, returning mock data
        return 22  # Placeholder
    
    def analyze_workload(self, request, queryset):
        """Analyze selected teachers' workloads using AI."""
        # Import the AI client lazily to avoid heavy imports at module load time
        try:
            from joyland.integrations.openai import OpenAIClient
        except Exception:
            OpenAIClient = None

        ai_client = OpenAIClient() if OpenAIClient is not None else None

        for teacher in queryset:
            try:
                # Get teacher's assignments
                assignments = self._get_teacher_assignments(teacher)
                # Get AI analysis (if available)
                analysis = ai_client.analyze_teacher_workload(assignments) if ai_client else {'warnings': [], 'recommendations': []}
                
                if analysis['warnings']:
                    self.message_user(
                        request,
                        format_html(
                            'Workload warnings for {}: {}',
                            teacher.get_full_name(),
                            '<br>'.join(f'• {w}' for w in analysis['warnings'])
                        ),
                        level=messages.WARNING
                    )
                
                if analysis['recommendations']:
                    self.message_user(
                        request,
                        format_html(
                            'Recommendations for {}: {}',
                            teacher.get_full_name(),
                            '<br>'.join(f'• {r}' for r in analysis['recommendations'])
                        ),
                        level=messages.INFO
                    )
                
            except Exception as e:
                logger.error(
                    'Failed to analyze workload for teacher: %s',
                    teacher.username,
                    exc_info=e
                )
                self.message_user(
                    request,
                    f'Error analyzing workload for {teacher.get_full_name()}',
                    level=messages.ERROR
                )
    
    analyze_workload.short_description = "Analyze selected teachers' workload"
    
    def _get_teacher_assignments(self, teacher):
        """Get teacher's current assignments."""
        # This would normally query your assignments model
        # For demo, returning mock data
        return [
            {
                'subject': 'Mathematics',
                'grade': '9th',
                'students': 25,
                'hours_per_week': 8
            },
            {
                'subject': 'Physics',
                'grade': '10th',
                'students': 30,
                'hours_per_week': 6
            }
        ]  # Placeholder data


class PrincipalProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'email', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')


custom_admin_site.register(StaffProfile, StaffProfileAdmin)
custom_admin_site.register(PrincipalProfile, PrincipalProfileAdmin)


"""
Announcement / RegistrationRequest / Event admin were removed from users.admin
They are owned by the core app and registered in core.admin to avoid duplicate
registration errors during app loading. See core/admin.py for those admin classes.
"""

