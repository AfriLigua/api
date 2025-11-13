from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    TutorViewSet, StudentViewSet,
    StudentRegistrationView, AdminRegistrationView,
    TutorRegistrationView, AdminLoginView, LoginView
)

router = DefaultRouter()
router.register(r'tutors', TutorViewSet, basename='tutors')
router.register(r'students', StudentViewSet, basename='students')

urlpatterns = [
    path('register/student/', StudentRegistrationView.as_view(), name='student-register'),
    path('register/tutor/', TutorRegistrationView.as_view(), name='tutor-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('admin/register/', AdminRegistrationView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
] + router.urls  

