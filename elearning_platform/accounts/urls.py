from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StudentRegistrationView, TutorRegistrationView, LoginView

urlpatterns = [
    path('register/student/', StudentRegistrationView.as_view(), name='student-register'),
    path('register/tutor/', TutorRegistrationView.as_view(), name='tutor-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
