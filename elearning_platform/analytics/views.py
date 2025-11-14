from rest_framework import viewsets, permissions
from .models import Testimonial, StudentProgress
from .serializers import TestimonialSerializer, StudentProgressSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Testimonial.objects.select_related('student', 'tutor', 'booking').all()


class StudentProgressViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return StudentProgress.objects.select_related('student', 'lesson', 'course').all()
