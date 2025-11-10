from django.contrib import admin
from .models import AvailabilitySlot, Booking


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ['tutor', 'start_time', 'end_time', 'is_booked']
    list_filter = ['is_booked']
    search_fields = ['tutor__email']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'tutor', 'course', 'status', 'amount', 'created_at']
    list_filter = ['status']
    search_fields = ['student__email', 'tutor__email']
