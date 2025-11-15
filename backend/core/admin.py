from django.contrib import admin
from .models import Announcement, RegistrationRequest, Event


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'priority', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'message')


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'first_name', 'last_name', 'email', 'status', 'created_at')
    list_filter = ('user_type', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'location', 'is_public')
    list_filter = ('is_public',)
    search_fields = ('title', 'description', 'location')
