from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = (
        ('email', 'Email'),
        ('in_app', 'In-App'),
        ('both', 'Both'),
    )
    
    CATEGORY_CHOICES = (
        ('tutor_approval', 'Tutor Approval'),
        ('booking', 'Booking'),
        ('payment', 'Payment'),
        ('message', 'Message'),
        ('withdrawal', 'Withdrawal'),
        ('lesson', 'Lesson'),
        ('reminder', 'Reminder'),
        ('general', 'General'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='in_app')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    def mark_as_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
