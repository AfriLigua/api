from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

def send_verification_email(user):
    """
    Send verification email to user (student or tutor) after registration
    """
    if not user.email:
        return

    # Generate verification token
    token = user.generate_verification_token()
    verification_link = f"{settings.FRONTEND_URL}/verify-email/{token}/"

    subject = "Verify your AfriLingua account"
    message = render_to_string('emails/verify_email.html', {
        'user': user,
        'verification_link': verification_link,
        'year': timezone.now().year
    })

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = "html"  # Render as HTML
    email.send(fail_silently=False)


def notify_admin_new_tutor_signup(tutor_profile):
    """
    Notify admin when a new tutor registers
    """
    from django.contrib.auth.models import User
    admins = User.objects.filter(is_staff=True, is_superuser=True)
    admin_emails = [admin.email for admin in admins if admin.email]

    if not admin_emails:
        return

    subject = "New Tutor Registration - AfriLingua"
    message = render_to_string('emails/admin_notify_tutor_signup.html', {
        'tutor': tutor_profile,
        'admin_dashboard_link': settings.FRONTEND_URL + "/admin/tutors",
        'year': timezone.now().year
    })

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=admin_emails,
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)


def send_password_reset_email(user):
    """
    Send password reset email with token
    """
    token = user.generate_password_reset_token()
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{token}/"

    subject = "AfriLingua Password Reset Request"
    message = render_to_string('emails/password_reset.html', {
        'user': user,
        'reset_link': reset_link,
        'year': timezone.now().year
    })

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)


def send_admin_welcome_email(admin_user):
    """
    Send welcome email to a newly created admin
    """
    subject = "Welcome to AfriLingua Admin Console"
    message = render_to_string('emails/admin_welcome.html', {
        'user': admin_user,
        'year': timezone.now().year
    })

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[admin_user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)


def send_admin_login_alert(admin_user):
    """
    Send alert to admin when they log in
    """
    subject = "AfriLingua Admin Login Alert"
    message = render_to_string('emails/admin_login_alert.html', {
        'user': admin_user,
        'now': timezone.now(),
        'year': timezone.now().year
    })

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[admin_user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
