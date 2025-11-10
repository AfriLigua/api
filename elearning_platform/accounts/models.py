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
    price_per_lesson = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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
