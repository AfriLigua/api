from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('email_verified', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('admin', 'Admin'),
    )
    
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_token_created = models.DateTimeField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_token_created = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def generate_verification_token(self):
        self.email_verification_token = str(uuid.uuid4())
        self.email_verification_token_created = timezone.now()
        self.save()
        return self.email_verification_token
    
    def verify_email_token(self, token):
        from datetime import timedelta
        from django.conf import settings
        
        if self.email_verification_token != token:
            return False
        
        if not self.email_verification_token_created:
            return False
        
        expiry_time = self.email_verification_token_created + timedelta(
            minutes=settings.EMAIL_VERIFICATION_TIMEOUT_MINUTES
        )
        
        if timezone.now() > expiry_time:
            return False
        
        self.email_verified = True
        self.email_verification_token = None
        self.email_verification_token_created = None
        self.save()
        return True
    
    def generate_password_reset_token(self):
        self.password_reset_token = str(uuid.uuid4())
        self.password_reset_token_created = timezone.now()
        self.save()
        return self.password_reset_token
    
    def verify_password_reset_token(self, token):
        from datetime import timedelta
        from django.conf import settings
        
        if self.password_reset_token != token:
            return False
        
        if not self.password_reset_token_created:
            return False
        
        expiry_time = self.password_reset_token_created + timedelta(
            minutes=settings.PASSWORD_RESET_TIMEOUT_MINUTES
        )
        
        if timezone.now() > expiry_time:
            return False
        
        return True


class TutorProfile(models.Model):
    APPROVAL_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tutor_profile')
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    languages = models.CharField(max_length=255, blank=True, help_text='Comma-separated languages taught')
    price_per_lesson = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Hourly rate in USD')
    total_hours_taught = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Total hours taught across all students')
    instant_booking = models.BooleanField(default=False, help_text='Allow students to instantly book without approval')
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='pending')
    cv = models.FileField(upload_to='tutors/cvs/', blank=True, null=True)
    certificate = models.FileField(upload_to='tutors/certificates/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.IntegerField(default=0)
    courses_taught = models.IntegerField(default=0)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tutor_profiles'
        verbose_name = 'Tutor Profile'
        verbose_name_plural = 'Tutor Profiles'
    
    def __str__(self):
        return f"{self.user.email} - Tutor Profile"
    
    def update_rating(self, new_rating):
        total = self.rating * self.total_ratings
        self.total_ratings += 1
        self.rating = (total + new_rating) / self.total_ratings
        self.save()
    
    def get_commission_rate(self):
        if self.total_hours_taught < 50:
            return 0.33
        elif self.total_hours_taught < 100:
            return 0.28
        elif self.total_hours_taught < 200:
            return 0.23
        else:
            return 0.18
    
    def add_teaching_hours(self, hours):
        self.total_hours_taught += hours
        self.save()


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_profiles'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"{self.user.email} - Student Profile"


class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    can_approve_tutors = models.BooleanField(default=True)
    can_manage_payments = models.BooleanField(default=True)
    can_manage_users = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'admin_profiles'
        verbose_name = 'Admin Profile'
        verbose_name_plural = 'Admin Profiles'
    
    def __str__(self):
        return f"{self.user.email} - Admin Profile"
