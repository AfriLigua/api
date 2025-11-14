from rest_framework import generics, status, permissions, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend

from .models import CustomUser, TutorProfile, StudentProfile
from .serializers import (
    UserSerializer, StudentRegistrationSerializer, TutorRegistrationSerializer,
    TutorProfileSerializer, StudentProfileSerializer, LoginSerializer, AdminLoginSerializer
)
from .emails import send_verification_email, notify_admin_new_tutor_signup
from .permissions import IsAdmin


class StudentRegistrationView(generics.CreateAPIView):
    """Register new students"""
    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role='student')

        send_verification_email(user)

        return Response({
            'message': 'Student registration successful. Please check your email for verification.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)


class TutorRegistrationView(generics.CreateAPIView):
    """Register new tutors"""
    serializer_class = TutorRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role='tutor')

        TutorProfile.objects.create(user=user)
        send_verification_email(user)
        notify_admin_new_tutor_signup(user.tutor_profile)

        return Response({
            'message': 'Tutor registration successful. Please verify your email and wait for admin approval.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login for students and tutors"""
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


class AdminRegistrationView(generics.CreateAPIView):
    """Create admin accounts (superusers only)"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            role='admin'
        )

        admin_group, _ = Group.objects.get_or_create(name='AdminCounsel')
        user.groups.add(admin_group)

        subject = "Welcome to AfriLingua Admin Console"
        message = render_to_string('emails/admin_welcome.html', {'user': user})
        send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)

        return Response({
            'message': 'Admin account created successfully',
            'email': user.email
        }, status=status.HTTP_201_CREATED)


class AdminLoginView(APIView):
    """Login for admin users"""
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


class TutorViewSet(viewsets.ModelViewSet):
    """
    Admin endpoints for managing tutors (list, retrieve, update, delete, approve, reject)
    Note: POST/create is disabled - use /register/tutor/ instead
    """
    serializer_class = TutorProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['approval_status', 'is_featured']
    search_fields = ['user__first_name', 'user__last_name', 'skills', 'bio']
    ordering_fields = ['rating', 'created_at']

    def get_queryset(self):
        return TutorProfile.objects.select_related('user').all()

    def get_permissions(self):
        if self.action in ['approve', 'reject', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [p() for p in permission_classes]

    def create(self, request, *args, **kwargs):
        """Disabled - use /register/tutor/ endpoint instead"""
        return Response(
            {'error': 'Use /api/v1/auth/register/tutor/ to register new tutors'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        tutor = self.get_object()
        tutor.approval_status = 'approved'
        tutor.save()
        return Response({'status': 'Tutor approved'})

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        tutor = self.get_object()
        tutor.approval_status = 'rejected'
        tutor.save()
        return Response({'status': 'Tutor rejected'})


class StudentViewSet(viewsets.ModelViewSet):
    """
    Admin endpoints for managing students (list, retrieve, update, delete)
    Note: POST/create is disabled - use /register/student/ instead
    """
    serializer_class = StudentProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'language', 'country']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return StudentProfile.objects.select_related('user').all()

    def get_permissions(self):
        permission_classes = [IsAdmin]
        return [p() for p in permission_classes]

    def create(self, request, *args, **kwargs):
        """Disabled - use /register/student/ endpoint instead"""
        return Response(
            {'error': 'Use /api/v1/auth/register/student/ to register new students'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
