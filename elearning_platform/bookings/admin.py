from django.contrib import admin
from .models import AvailabilitySlot, Booking, Lesson, Subscription, Classroom


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ['tutor', 'start_time', 'end_time', 'is_booked']
    list_filter = ['is_booked']
    search_fields = ['tutor__email']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'tutor', 'course', 'is_trial_lesson', 'status', 'amount', 'created_at']
    list_filter = ['status', 'is_trial_lesson']
    search_fields = ['student__email', 'tutor__email']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'is_trial', 'is_confirmed', 'confirmed_by', 'duration_minutes', 'created_at']
    list_filter = ['is_trial', 'is_confirmed', 'confirmed_by']
    search_fields = ['booking__student__email', 'booking__tutor__email']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'tutor', 'plan_type', 'status', 'price_per_lesson', 'renewal_date', 'created_at']
    list_filter = ['status', 'plan_type']
    search_fields = ['student__email', 'tutor__email']
    actions = ['pause_subscriptions', 'resume_subscriptions', 'cancel_subscriptions']
    
    def pause_subscriptions(self, request, queryset):
        for subscription in queryset:
            subscription.pause()
    
    def resume_subscriptions(self, request, queryset):
        for subscription in queryset:
            subscription.resume()
    
    def cancel_subscriptions(self, request, queryset):
        for subscription in queryset:
            subscription.cancel()


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'video_session_link', 'session_started_at', 'session_ended_at', 'created_at']
    search_fields = ['lesson__booking__student__email', 'lesson__booking__tutor__email']
