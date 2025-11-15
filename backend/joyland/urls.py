from django.urls import path, include
from django.views.generic import TemplateView
from users.admin_site import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    # placeholders
    path('curriculum/', TemplateView.as_view(template_name='placeholders/curriculum.html'), name='curriculum'),
    path('branches/main/', TemplateView.as_view(template_name='placeholders/branches_main.html'), name='branches_main'),
    path('branches/joyland-mambowe/', TemplateView.as_view(template_name='placeholders/branches_joyland_mambowe.html'), name='branches_mambowe'),
    path('admissions/join-us/', TemplateView.as_view(template_name='placeholders/admissions_join_us.html'), name='admissions_join'),
    path('admissions/appointment/', TemplateView.as_view(template_name='placeholders/admissions_appointment.html'), name='admissions_appointment'),
    path('admissions/process/', TemplateView.as_view(template_name='placeholders/admissions_process.html'), name='admissions_process'),
    path('admissions/term-dates-2025-26/', TemplateView.as_view(template_name='placeholders/admissions_term_dates_2025_26.html'), name='admissions_terms'),
    path('admissions/school-fees-2025-26/', TemplateView.as_view(template_name='placeholders/admissions_school_fees_2025_26.html'), name='admissions_fees'),
    path('admissions/online-test/', TemplateView.as_view(template_name='placeholders/admissions_online_test.html'), name='admissions_test'),
    path('vacancies/', TemplateView.as_view(template_name='placeholders/vacancies.html'), name='vacancies'),
    path('contact/', TemplateView.as_view(template_name='placeholders/contact.html'), name='contact'),
    path('users/parents-access/', TemplateView.as_view(template_name='placeholders/parents_portal.html'), name='parents_portal'),
]
