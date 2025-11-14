from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, CourseListSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Course.objects.select_related('created_by').all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Lesson.objects.select_related('course').all()
