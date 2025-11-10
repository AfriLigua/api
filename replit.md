# E-Learning Platform - Django REST Framework Backend

## Overview
A comprehensive production-ready Django REST Framework backend for an E-Learning Platform with role-based access control, payment processing, messaging, and analytics. Built for Replit deployment with PostgreSQL database support.

## Project Status
**Current State**: Initial MVP implementation complete and running
**Last Updated**: November 10, 2025

## Core Features Implemented

### Authentication & User Management
- JWT-based authentication with refresh tokens
- Role-based access control (Student, Tutor, Admin)
- Custom User model with email as username
- Student registration with immediate access
- Tutor registration with admin approval workflow
- Email verification system (10-minute token expiry)
- Password reset functionality (10-minute token expiry)

### User Profiles
- **TutorProfile**: Bio, skills, pricing, CV/certificate uploads, approval status, ratings, wallet balance
- **StudentProfile**: Bio, language, country, multi-currency support
- Profile management endpoints

### Courses & Lessons
- Course CRUD operations with categories
- Lesson management with video URLs and file uploads
- Course publishing system
- Tutor-created courses with price setting

### Bookings & Availability
- Availability slot management for tutors
- Booking creation and management
- Double-booking prevention through unique constraints
- Duration-based pricing calculation
- Platform fee calculation (15% platform, 85% tutor)
- Booking status tracking (pending, paid, confirmed, completed, cancelled, refunded)
- Refund eligibility based on cutoff hours (24hrs before)

### Payment System
- Payment model with Stripe/PayPal/Wise support
- Transaction tracking with status management
- Tutor wallet system (available, pending, total earned balances)
- Withdrawal request system with admin approval
- Multi-currency support

### Messaging
- Conversation management
- Message creation and retrieval
- Restricted to active bookings/enrolled courses
- Read status tracking

### Notifications
- In-app notification system
- Multiple notification categories (tutor_approval, booking, payment, message, withdrawal, lesson, reminder)
- Read/unread status tracking
- Notification metadata support

### Analytics & Testimonials
- Student progress tracking per lesson
- Testimonial system with ratings (1-5 stars)
- Audit logging for user actions
- IP address and user agent tracking

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/student/` - Student registration
- `POST /api/v1/auth/register/tutor/` - Tutor registration (requires CV & certificate)
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token

### Courses & Lessons
- `GET/POST /api/v1/courses/` - List/Create courses
- `GET/PUT/PATCH/DELETE /api/v1/courses/{id}/` - Course detail operations
- `GET/POST /api/v1/lessons/` - List/Create lessons
- `GET/PUT/PATCH/DELETE /api/v1/lessons/{id}/` - Lesson detail operations

### Bookings
- `GET/POST /api/v1/availability-slots/` - Manage tutor availability
- `GET/POST /api/v1/bookings/` - Manage bookings
- `GET/PUT/PATCH/DELETE /api/v1/bookings/{id}/` - Booking detail operations

### Payments
- `GET /api/v1/payments/` - List payments
- `GET /api/v1/wallets/` - Tutor wallet information
- `GET/POST /api/v1/withdrawals/` - Withdrawal requests

### Messaging
- `GET/POST /api/v1/conversations/` - Manage conversations
- `GET/POST /api/v1/messages/` - Send/retrieve messages

### Notifications
- `GET /api/v1/notifications/` - User notifications

### Analytics
- `GET/POST /api/v1/testimonials/` - Testimonials and ratings
- `GET/POST /api/v1/progress/` - Student progress tracking

## Database Models

### Accounts App
- **CustomUser**: Email-based authentication, roles, verification tokens
- **TutorProfile**: Tutor-specific data, approval status, wallet
- **StudentProfile**: Student-specific data, preferences

### Courses App
- **Course**: Title, description, category, pricing, publish status
- **Lesson**: Content, videos, files, duration, ordering

### Bookings App
- **AvailabilitySlot**: Tutor schedule with booking status
- **Booking**: Student-tutor bookings with payment tracking

### Payments App
- **Payment**: Transaction records with provider info
- **TutorWallet**: Balance management (available/pending/total)
- **WithdrawalRequest**: Tutor payout requests with admin approval

### Messaging App
- **Conversation**: Multi-participant conversations
- **Message**: Individual messages with read status

### Notifications App
- **Notification**: User notifications with categories and types

### Analytics App
- **Testimonial**: Student ratings and reviews for tutors
- **StudentProgress**: Lesson completion tracking
- **AuditLog**: System activity logging

## Technology Stack

### Core Framework
- **Django**: 4.2.7
- **Django REST Framework**: 3.14.0
- **Python**: 3.11

### Authentication & Security
- **djangorestframework-simplejwt**: JWT tokens
- **django-cors-headers**: CORS support
- **Password validators**: Django built-in

### Database
- **PostgreSQL**: Production database (via DATABASE_URL)
- **SQLite**: Local development fallback
- **psycopg2-binary**: PostgreSQL adapter

### Async Tasks (Ready for implementation)
- **Celery**: 5.3.4
- **Redis**: 5.0.1

### Payment Integration (Ready for implementation)
- **Stripe**: Python SDK 7.4.0

### Additional Packages
- **Pillow**: Image handling
- **django-filter**: Advanced filtering
- **python-decouple**: Environment variables
- **dj-database-url**: Database configuration
- **gunicorn**: Production WSGI server
- **reportlab**: PDF generation

## Environment Configuration

### Required Environment Variables
```
DATABASE_URL=postgresql://...
SECRET_KEY=...
DEBUG=True/False
ALLOWED_HOSTS=*

# Email settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587

# Payment providers (to be configured)
STRIPE_SECRET_KEY=...
STRIPE_PUBLISHABLE_KEY=...

# Celery/Redis (to be configured)
CELERY_BROKER_URL=redis://localhost:6379/0

# Platform settings
PLATFORM_FEE_PERCENTAGE=15
DEFAULT_CURRENCY=USD
BOOKING_REFUND_CUTOFF_HOURS=24
```

## Security Features
- CORS configured for cross-origin requests
- JWT authentication with token rotation
- Password validation with strength requirements
- Email verification for new accounts
- Time-limited password reset tokens
- Role-based permissions on all endpoints
- Audit logging for critical actions

## Next Phase Implementation

### Immediate Priorities
1. **Celery Tasks**: Notifications, reminders, automated payouts
2. **Stripe Integration**: Payment processing webhooks
3. **Admin Dashboard**: Analytics endpoints, reporting
4. **Email Templates**: Branded transactional emails
5. **Advanced Booking Features**: Reschedule, refund workflows
6. **Find Tutors**: Advanced filtering endpoint

### Future Enhancements
1. **Two-Factor Authentication** (2FA) for tutors/admins
2. **Zoom/Google Meet Integration** for video links
3. **PayPal & Wise Integration** for additional payment methods
4. **Automated Reminders**: 1hr/24hr before lessons
5. **CSV/PDF Export**: Admin reports
6. **Cloud Storage**: AWS S3 for media files

## Development Notes
- All migrations applied successfully
- Server running on port 5000 (webview)
- Django admin available at `/admin/`
- API base URL: `/api/v1/`
- Media files stored in `/media/`
- Static files in `/staticfiles/`

## Admin Access
To create a superuser:
```bash
python manage.py createsuperuser
```

## API Testing
Use tools like:
- Postman
- cURL
- Django REST Framework Browsable API (when DEBUG=True)

## Git Configuration
`.gitignore` includes:
- Python cache files
- Media uploads
- Database files
- Environment variables (.env)
- Log files
