from django.db import models
from django.conf import settings
from django.utils import timezone


class AvailabilitySlot(models.Model):
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availability_slots'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'availability_slots'
        verbose_name = 'Availability Slot'
        verbose_name_plural = 'Availability Slots'
        ordering = ['start_time']
        unique_together = ['tutor', 'start_time', 'end_time']
    
    def __str__(self):
        return f"{self.tutor.email} - {self.start_time} to {self.end_time}"
    
    def get_duration_minutes(self):
        duration = self.end_time - self.start_time
        return int(duration.total_seconds() / 60)


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_bookings'
    )
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutor_bookings'
    )
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='bookings')
    availability_slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.CASCADE,
        related_name='booking'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tutor_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    meeting_link = models.URLField(blank=True, null=True)
    reschedule_reason = models.TextField(blank=True, null=True)
    refund_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.student.email} with {self.tutor.email}"
    
    def calculate_fees(self):
        platform_fee_percentage = settings.PLATFORM_FEE_PERCENTAGE / 100
        self.platform_fee = self.amount * platform_fee_percentage
        self.tutor_earnings = self.amount - self.platform_fee
        self.save()
    
    def can_refund(self):
        from datetime import timedelta
        cutoff_time = self.availability_slot.start_time - timedelta(
            hours=settings.BOOKING_REFUND_CUTOFF_HOURS
        )
        return timezone.now() < cutoff_time
