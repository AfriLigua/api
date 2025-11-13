from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StudentRegistrationView, AdminRegistrationView, TutorRegistrationView, AdminLoginView,  LoginView 

urlpatterns = [
    path('register/student/', StudentRegistrationView.as_view(), name='student-register'),
    path('register/tutor/', TutorRegistrationView.as_view(), name='tutor-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('admin/register/', AdminRegistrationView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
]
