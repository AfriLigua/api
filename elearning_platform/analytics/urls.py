from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestimonialViewSet, StudentProgressViewSet

router = DefaultRouter()
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'progress', StudentProgressViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),
]
