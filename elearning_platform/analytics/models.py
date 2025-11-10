from django.db import models
from django.conf import settings


class Testimonial(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='testimonials_given'
    )
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='testimonials_received'
    )
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='testimonials',
        blank=True,
        null=True
    )
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'testimonials'
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-created_at']
        unique_together = ['student', 'booking']
    
    def __str__(self):
        return f"{self.student.email} → {self.tutor.email} - {self.rating} stars"


class StudentProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE, related_name='student_progress')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='student_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    time_spent = models.IntegerField(default=0, help_text='Time spent in minutes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_progress'
        verbose_name = 'Student Progress'
        verbose_name_plural = 'Student Progress'
        unique_together = ['student', 'lesson']
    
    def __str__(self):
        return f"{self.student.email} - {self.lesson.title}"
    
    def mark_completed(self):
        from django.utils import timezone
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.save()


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Profile Update'),
        ('booking_created', 'Booking Created'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('payment_made', 'Payment Made'),
        ('withdrawal_requested', 'Withdrawal Requested'),
        ('withdrawal_processed', 'Withdrawal Processed'),
        ('course_created', 'Course Created'),
        ('course_updated', 'Course Updated'),
        ('tutor_approved', 'Tutor Approved'),
        ('tutor_rejected', 'Tutor Rejected'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='audit_logs',
        null=True,
        blank=True
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        user_email = self.user.email if self.user else 'Unknown'
        return f"{user_email} - {self.action} - {self.created_at}"
