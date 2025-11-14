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
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='bookings', blank=True, null=True)
    subscription = models.ForeignKey(
        'Subscription',
        on_delete=models.SET_NULL,
        related_name='bookings',
        blank=True,
        null=True,
        help_text='If this booking is part of a subscription'
    )
    availability_slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.CASCADE,
        related_name='booking'
    )
    is_trial_lesson = models.BooleanField(default=False, help_text='First lesson with this tutor')
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
    
    def can_reschedule_or_cancel(self):
        from datetime import timedelta
        cutoff_time = self.availability_slot.start_time - timedelta(
            hours=settings.BOOKING_RESCHEDULE_CANCEL_CUTOFF_HOURS
        )
        return timezone.now() < cutoff_time


class Lesson(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='lesson'
    )
    is_trial = models.BooleanField(default=False, help_text='Is this the student\'s first lesson with this tutor?')
    is_confirmed = models.BooleanField(default=False)
    confirmed_by = models.CharField(max_length=20, choices=(('student', 'Student'), ('tutor', 'Tutor'), ('auto', 'Automatic')), blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(default=60)
    notes = models.TextField(blank=True, help_text='Lesson notes from tutor')
    homework = models.TextField(blank=True, help_text='Homework assigned to student')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tutoring_lessons'
        verbose_name = 'Tutoring Lesson'
        verbose_name_plural = 'Tutoring Lessons'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Lesson #{self.id} - Booking #{self.booking.id}"
    
    def auto_confirm(self):
        from datetime import timedelta
        if not self.is_confirmed:
            scheduled_end = self.booking.availability_slot.end_time
            auto_confirm_time = scheduled_end + timedelta(minutes=15)
            if timezone.now() >= auto_confirm_time:
                self.is_confirmed = True
                self.confirmed_by = 'auto'
                self.confirmed_at = timezone.now()
                self.save()
                return True
        return False


class Subscription(models.Model):
    PLAN_CHOICES = (
        ('1_per_week', '1 Lesson per Week'),
        ('2_per_week', '2 Lessons per Week'),
        ('3_per_week', '3 Lessons per Week'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
    )
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutor_subscriptions'
    )
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='1_per_week')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    price_per_lesson = models.DecimalField(max_digits=10, decimal_places=2)
    lessons_per_billing_cycle = models.IntegerField(default=4, help_text='Number of lessons in 28-day cycle')
    unused_lessons = models.IntegerField(default=0, help_text='Carry-over lessons from previous cycle')
    renewal_date = models.DateField()
    next_billing_date = models.DateField()
    started_at = models.DateTimeField(auto_now_add=True)
    paused_at = models.DateTimeField(blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'tutor'],
                condition=models.Q(status__in=['active', 'paused']),
                name='unique_active_subscription_per_tutor'
            )
        ]
    
    def __str__(self):
        return f"{self.student.email} → {self.tutor.email} - {self.plan_type}"
    
    def pause(self):
        if self.status == 'active':
            self.status = 'paused'
            self.paused_at = timezone.now()
            self.save()
    
    def resume(self):
        if self.status == 'paused':
            self.status = 'active'
            self.paused_at = None
            self.save()
    
    def cancel(self):
        self.status = 'canceled'
        self.canceled_at = timezone.now()
        self.save()


class Classroom(models.Model):
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name='classroom'
    )
    video_session_link = models.URLField(blank=True, null=True, help_text='Link to video call session')
    whiteboard_notes = models.TextField(blank=True, help_text='Notes from whiteboard')
    shared_files = models.JSONField(default=list, blank=True, help_text='List of file URLs shared during lesson')
    recording_url = models.URLField(blank=True, null=True, help_text='Lesson recording URL')
    session_started_at = models.DateTimeField(blank=True, null=True)
    session_ended_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'classrooms'
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'
    
    def __str__(self):
        return f"Classroom - Lesson #{self.lesson.id}"
