from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TutorProfile, StudentProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'email_verified', 'is_active', 'created_at']
    list_filter = ['role', 'email_verified', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'approval_status', 'rating', 'courses_taught', 'wallet_balance', 'is_featured']
    list_filter = ['approval_status', 'is_featured']
    search_fields = ['user__email', 'skills']
    actions = ['approve_tutors', 'reject_tutors']
    
    def approve_tutors(self, request, queryset):
        queryset.update(approval_status='approved')
    
    def reject_tutors(self, request, queryset):
        queryset.update(approval_status='rejected')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'language', 'currency', 'created_at']
    list_filter = ['currency', 'country']
    search_fields = ['user__email', 'country']
