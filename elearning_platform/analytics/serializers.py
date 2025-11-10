from rest_framework import serializers
from .models import Testimonial, StudentProgress, AuditLog


class TestimonialSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)
    tutor_email = serializers.EmailField(source='tutor.email', read_only=True)
    
    class Meta:
        model = Testimonial
        fields = '__all__'
        read_only_fields = ['student', 'tutor', 'is_approved', 'created_at', 'updated_at']


class StudentProgressSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = StudentProgress
        fields = '__all__'
        read_only_fields = ['student', 'is_completed', 'completed_at', 'created_at', 'updated_at']


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = '__all__'
