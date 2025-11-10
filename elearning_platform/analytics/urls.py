from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestimonialViewSet, StudentProgressViewSet

router = DefaultRouter()
router.register(r'testimonials', TestimonialViewSet)
router.register(r'progress', StudentProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
