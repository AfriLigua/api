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


from .serializers import LoginSerializer, UserSerializer

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

        
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
from .serializers import AdminLoginSerializer

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

# ------------------- ADMIN LOGIN -------------------
class AdminLoginView(APIView):
    serializer_class = AdminLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if not user or user.role != 'admin':
            return Response({'error': 'Invalid credentials or not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TutorProfile, StudentProfile
from .serializers import TutorProfileSerializer, StudentProfileSerializer
from .permissions import IsAdmin


# -------------------------------
# Tutors CRUD + Approve/Reject
# -------------------------------
class TutorViewSet(viewsets.ModelViewSet):
    queryset = TutorProfile.objects.all()
    serializer_class = TutorProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['approval_status', 'is_featured']
    search_fields = ['user__first_name', 'user__last_name', 'skills', 'bio']
    ordering_fields = ['rating', 'created_at']

    def get_permissions(self):
        if self.action in ['approve', 'reject']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [p() for p in permission_classes]

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        tutor = self.get_object()
        tutor.approval_status = 'approved'
        tutor.save()
        # TODO: Send email notification to tutor
        return Response({'status': 'Tutor approved'})

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        tutor = self.get_object()
        tutor.approval_status = 'rejected'
        tutor.save()
        # TODO: Send email notification to tutor
        return Response({'status': 'Tutor rejected'})


# -------------------------------
# Students CRUD
# -------------------------------
class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'language', 'country']
    ordering_fields = ['created_at']

    def get_permissions(self):
        # Only admin can list all students
        permission_classes = [IsAdmin]
        return [p() for p in permission_classes]
