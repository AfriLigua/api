from django.contrib import admin
from .models import Testimonial, StudentProgress, AuditLog


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'tutor', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved']
    search_fields = ['student__email', 'tutor__email']
    actions = ['approve_testimonials']
    
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'lesson', 'is_completed', 'time_spent']
    list_filter = ['is_completed']
    search_fields = ['student__email']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'action', 'ip_address', 'created_at']
    list_filter = ['action']
    search_fields = ['user__email', 'description']
    readonly_fields = ['user', 'action', 'description', 'ip_address', 'user_agent', 'metadata', 'created_at']
