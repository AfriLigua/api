from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import CustomUser, TutorProfile, StudentProfile
from .serializers import (
    UserSerializer, StudentRegistrationSerializer, TutorRegistrationSerializer,
    TutorProfileSerializer, StudentProfileSerializer, EmailVerificationSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from .emails import (
    send_verification_email,
    send_password_reset_email,
    notify_admin_new_tutor_signup
)


class StudentRegistrationView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role='student')

        # Send verification + welcome email
        send_verification_email(user)

        return Response({
            'message': 'Student registration successful. Please check your email for verification.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)


class TutorRegistrationView(generics.CreateAPIView):
    serializer_class = TutorRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role='tutor')

        # Create tutor profile automatically
        TutorProfile.objects.create(user=user)

        # Send verification email to tutor
        send_verification_email(user)

        # Notify admin for approval
        notify_admin_new_tutor_signup(user.tutor_profile)

        return Response({
            'message': 'Tutor registration successful. Please verify your email and wait for admin approval.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.role == 'tutor' and hasattr(user, 'tutor_profile'):
            if user.tutor_profile.approval_status != 'approved':
                return Response({'error': 'Your account is pending admin approval.'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            send_password_reset_email(user)
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth.models import Group


class AdminRegistrationView(generics.CreateAPIView):
    """
    Allows superusers to create admin accounts (for platform management)
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        # Create new admin user
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )

        # Optionally add to group
        admin_group, _ = Group.objects.get_or_create(name='AdminCounsel')
        user.groups.add(admin_group)

        # Send welcome email
        subject = "Welcome to AfriLingua Admin Console"
        message = render_to_string('emails/admin_welcome.html', {'user': user})
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)

        return Response({
            'message': 'Admin account created successfully',
            'email': user.email
        }, status=status.HTTP_201_CREATED)


class AdminLoginView(APIView):
    """
    Login for Admin Counsel users
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_staff and not user.is_superuser:
            return Response({'error': 'You do not have admin access'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        # Send login alert email
        subject = "AfriLingua Admin Login Alert"
        message = render_to_string('emails/admin_login_alert.html', {'user': user})
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)

        return Response({
            'message': 'Admin login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
