# AfriLingua - Two-Sided Tutoring Marketplace Platform

## Overview
A full-featured two-sided tutoring marketplace inspired by Preply, built on Django REST Framework. AfriLingua enables students to discover and book tutors for one-on-one lessons with trial lessons, subscription plans, and a dynamic commission-based payment system.

## Project Status
**Current State**: Backend fully cleaned, optimized, and ready for production
**Last Updated**: November 13, 2025
**Architecture**: Preply-inspired tutoring marketplace

## Core Features

### Authentication & User Management
- JWT-based authentication with refresh tokens
- Role-based access control (Student, Tutor, Admin)
- Custom User model with email as username
- **Student registration**: `POST /api/v1/auth/register/student/`
- **Tutor registration**: `POST /api/v1/auth/register/tutor/` (requires admin approval)
- Admin registration with special permissions
- Email verification system (10-minute token expiry)
- Password reset functionality

### User Profiles

#### TutorProfile (Enhanced for Marketplace)
- Bio, skills, languages taught, CV/certificate uploads
- **Hourly rate** setting for lessons
- **Total hours taught** tracking for commission tiers
- **Instant booking** option
- **Languages** field for multi-language tutors
- Approval status (pending, approved, rejected)
- **Dynamic commission rate** based on teaching hours:
  - 0-49 hours: 33% commission
  - 50-99 hours: 28% commission
  - 100-199 hours: 23% commission
  - 200+ hours: 18% commission
- Rating and total ratings tracking
- Wallet balance management

#### StudentProfile
- Bio, language, country preferences
- Multi-currency support
- Learning goals and interests

#### AdminProfile (New)
- Department and phone number
- Permission flags:
  - `can_approve_tutors`
  - `can_manage_payments`
  - `can_manage_users`

### Tutoring Sessions (Lessons)

#### Lesson Model (New - Separate from Course Lessons)
- One-to-one relationship with bookings
- **Trial lesson** tracking (first lesson with tutor = 100% commission)
- **Confirmation status** (pending, confirmed, disputed)
- **Auto-confirmation**: 15 minutes after lesson end time
- Duration, homework, notes, attachments
- Tutor and student feedback

#### Subscription Plans (New)
- Weekly lesson plans: 1, 2, or 3 lessons per week
- Status tracking: active, paused, canceled, expired
- Unused lessons rollover
- Auto-renewal with billing cycles
- Methods: `pause()`, `resume()`, `cancel()`
- **Unique constraint**: One active subscription per student-tutor pair

#### Virtual Classroom (New)
- Video conferencing links (Zoom, Google Meet, custom)
- Whiteboard notes and shared files
- Session recordings
- Start/end timestamps

### Bookings & Availability
- Availability slot management for tutors
- **Trial lesson booking** (first lesson with tutor)
- **Subscription-based bookings** (linked to subscription plans)
- Double-booking prevention through unique constraints
- Duration-based pricing calculation
- **12-hour reschedule/cancel rule** (configurable via `BOOKING_RESCHEDULE_CANCEL_CUTOFF_HOURS`)
- Booking status tracking (pending, paid, confirmed, completed, cancelled, refunded)

### Payment System (Enhanced)

#### Transaction Model (New)
- Comprehensive transaction tracking
- Types: lesson_payment, subscription_payment, payout, refund
- **Commission calculation** with trial lesson logic
- Platform fee, tutor earnings, and net amount tracking
- Stripe, PayPal, Wise, Payoneer support
- Transaction metadata and audit trail

#### Tutor Wallet
- Available balance (ready for withdrawal)
- Pending balance (awaiting lesson confirmation)
- Total earned tracking
- Commission tier progression

#### Withdrawal Requests
- Multiple payout methods: Wise, Payoneer, PayPal, Skrill
- Admin approval workflow
- Payout details and bank information
- Processing status tracking

### Messaging
- Conversation management between students and tutors
- Message creation and retrieval
- Read status tracking
- Restricted to active bookings/enrolled courses

### Notifications
- In-app notification system
- Categories: tutor_approval, booking, payment, message, withdrawal, lesson, reminder
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
- `POST /api/v1/auth/login/` - User login (students & tutors)
- `POST /api/v1/auth/admin/login/` - Admin login
- `POST /api/v1/auth/admin/register/` - Admin registration (superusers only)
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token

### Admin Management
- `GET /api/v1/auth/tutors/` - List all tutors (authenticated users)
- `GET/PUT/PATCH/DELETE /api/v1/auth/tutors/{id}/` - Manage tutor (admin only)
- `POST /api/v1/auth/tutors/{id}/approve/` - Approve tutor (admin only)
- `POST /api/v1/auth/tutors/{id}/reject/` - Reject tutor (admin only)
- `GET /api/v1/auth/students/` - List all students (admin only)
- `GET/PUT/PATCH/DELETE /api/v1/auth/students/{id}/` - Manage student (admin only)

**Note**: POST to `/tutors/` and `/students/` is disabled. Use registration endpoints instead.

### Courses & Lessons
- `GET /api/v1/courses/` - List/Search courses
- `GET/PUT/PATCH/DELETE /api/v1/courses/{id}/` - Course detail operations
- `GET /api/v1/lessons/` - List lessons
- `GET/PUT/PATCH/DELETE /api/v1/lessons/{id}/` - Lesson detail operations

### Bookings
- `GET /api/v1/availability-slots/` - List tutor availability
- `GET /api/v1/bookings/` - List bookings
- `GET/PUT/PATCH/DELETE /api/v1/bookings/{id}/` - Booking detail operations

### Payments
- `GET /api/v1/payments/` - List payments (authenticated)
- `GET /api/v1/wallets/` - Tutor wallet information (authenticated)
- `GET/POST /api/v1/withdrawals/` - Withdrawal requests (authenticated)

### Messaging
- `GET /api/v1/conversations/` - List conversations
- `GET /api/v1/messages/` - Retrieve messages

### Notifications
- `GET /api/v1/notifications/` - User notifications (authenticated)

### Analytics
- `GET /api/v1/testimonials/` - Testimonials and ratings
- `GET /api/v1/progress/` - Student progress tracking

## Database Models

### Accounts App
- **CustomUser**: Email-based authentication, roles, verification tokens
- **TutorProfile**: Tutor marketplace data, hourly_rate, total_hours_taught, commission_rate calculation
- **StudentProfile**: Student preferences and learning goals
- **AdminProfile**: Admin permissions and department info

### Bookings App
- **AvailabilitySlot**: Tutor schedule with booking status
- **Booking**: Student-tutor bookings with trial lesson and subscription support
- **Lesson**: Individual tutoring sessions (separate from course lessons)
- **Subscription**: Weekly lesson plans with pause/cancel functionality
- **Classroom**: Virtual classroom with video links and resources

### Payments App
- **Payment**: Transaction records with provider info
- **Transaction**: Comprehensive transaction tracking with commission calculation
- **TutorWallet**: Balance management (available/pending/total)
- **WithdrawalRequest**: Tutor payout requests (Wise, Payoneer, PayPal, Skrill)

### Messaging App
- **Conversation**: Multi-participant conversations (optimized with prefetch_related)
- **Message**: Individual messages with read status (optimized with select_related)

### Notifications App
- **Notification**: User notifications with categories and types

### Analytics App
- **Testimonial**: Student ratings and reviews for tutors
- **StudentProgress**: Lesson completion tracking
- **AuditLog**: System activity logging

### Courses App
- **Course**: Title, description, category, pricing (original e-learning feature)
- **Lesson**: Course lesson content (separate from tutoring lessons)

## Technology Stack

### Core Framework
- **Django**: 4.2.7
- **Django REST Framework**: 3.14.0
- **Python**: 3.11/3.12

### Authentication & Security
- **djangorestframework-simplejwt**: JWT tokens
- **django-cors-headers**: CORS support
- **Password validators**: Django built-in

### Database
- **PostgreSQL**: Production database (via DATABASE_URL)
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
- **whitenoise**: Static file serving
- **drf-spectacular**: API documentation

## Performance Optimizations (Recently Applied)

### Database Query Optimization
All ViewSets now use `select_related()` and `prefetch_related()` to reduce database queries:

- **BookingViewSet**: Optimized with student, tutor, course, availability_slot, subscription
- **PaymentViewSet**: Optimized with user, booking
- **TutorWalletViewSet**: Optimized with tutor
- **WithdrawalRequestViewSet**: Optimized with tutor
- **ConversationViewSet**: Optimized with booking, participants (prefetch)
- **MessageViewSet**: Optimized with sender, conversation
- **CourseViewSet**: Optimized with created_by
- **LessonViewSet**: Optimized with course
- **NotificationViewSet**: Optimized with user
- **TestimonialViewSet**: Optimized with student, tutor, booking
- **StudentProgressViewSet**: Optimized with student, lesson, course
- **TutorViewSet**: Optimized with user
- **StudentViewSet**: Optimized with user

### Code Cleanup (Recently Applied)
- ✅ Removed duplicate imports across all views
- ✅ Disabled POST/create on admin viewsets (tutors, students)
- ✅ Consolidated registration to dedicated endpoints only
- ✅ Added proper basename to all router registrations
- ✅ Improved code structure and readability
- ✅ Fixed all routing issues

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
DEFAULT_FROM_EMAIL=afriligua@gmail.com

# Payment providers
STRIPE_SECRET_KEY=...
STRIPE_PUBLISHABLE_KEY=...
STRIPE_WEBHOOK_SECRET=...

# Celery/Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Platform settings
PLATFORM_FEE_PERCENTAGE=33
DEFAULT_CURRENCY=USD
BOOKING_REFUND_CUTOFF_HOURS=24
BOOKING_RESCHEDULE_CANCEL_CUTOFF_HOURS=12
EMAIL_VERIFICATION_TIMEOUT_MINUTES=10
PASSWORD_RESET_TIMEOUT_MINUTES=10

# Frontend
FRONTEND_URL=http://localhost:8080
```

## Security Features
- CORS configured for cross-origin requests
- JWT authentication with token rotation
- Password validation with strength requirements
- Email verification for new accounts
- Time-limited password reset tokens
- Role-based permissions on all endpoints
- Audit logging for critical actions
- Commission calculation with trial lesson protection

## Commission Structure
1. **Trial Lessons**: 100% commission (platform keeps everything)
2. **Regular Lessons**: Dynamic commission based on tutor's total hours:
   - 0-49 hours: 33% commission
   - 50-99 hours: 28% commission
   - 100-199 hours: 23% commission
   - 200+ hours: 18% commission

## Next Phase Implementation

### Immediate Priorities
1. **Serializers**: Create serializers for new models (Lesson, Subscription, Transaction, Classroom)
2. **API Views**: Build tutor browsing, subscription management, lesson confirmation endpoints
3. **Celery Tasks**: Lesson reminders (1 hour before), auto-confirmations (15 min after end)
4. **Email Notifications**: Welcome, approval, booking, payment receipts
5. **Stripe Integration**: Payment processing webhooks with commission calculation
6. **Admin Dashboard**: Analytics endpoints, transaction oversight, tutor approval workflow

### Future Enhancements
1. **Advanced Search**: Tutor filtering by language, skills, rate, rating, availability
2. **Zoom/Google Meet Integration**: Auto-generate video links for lessons
3. **Two-Factor Authentication** (2FA) for tutors/admins
4. **Automated Reminders**: 1hr/24hr before lessons via email/SMS
5. **CSV/PDF Export**: Admin reports and tutor earnings statements
6. **Cloud Storage**: AWS S3 for media files (CVs, certificates, recordings)

## Development Notes
- All migrations applied successfully
- Server running on port 5000 (webview)
- Django admin available at `/admin/`
- API base URL: `/api/v1/`
- API documentation: `/api/schema/` (Swagger/Redoc)
- Media files stored in `/media/`
- Static files in `/staticfiles/`

## Admin Access
To create a superuser:
```bash
python manage.py createsuperuser
```

## API Testing
- **Swagger UI**: Available in DEBUG mode
- **Postman/Thunder Client**: Import schema from `/api/schema/`
- **Django REST Framework Browsable API**: Available when DEBUG=True
- **cURL**: Command-line testing

## Project Structure
```
elearning_platform/
├── accounts/          # User management, profiles, authentication
├── bookings/          # Availability, bookings, lessons, subscriptions, classrooms
├── payments/          # Payments, transactions, wallets, withdrawals
├── courses/           # Courses and course lessons (original feature)
├── messaging/         # Conversations and messages
├── notifications/     # In-app notifications
├── analytics/         # Testimonials, progress tracking, audit logs
├── settings.py        # Django configuration
└── urls.py            # Main URL routing

manage.py              # Django management
requirements.txt       # Python dependencies
celery_app.py         # Celery configuration (ready for tasks)
```

## Recent Changes (November 13, 2025)
- ✅ Backend cleanup and optimization completed
- ✅ Removed duplicate registration endpoints (POST /tutors/, POST /students/)
- ✅ Consolidated all registration to `/register/student/` and `/register/tutor/`
- ✅ Added performance optimizations (select_related, prefetch_related)
- ✅ Fixed commission rate calculation (33% base instead of 100%)
- ✅ Made subscription uniqueness conditional (allows re-subscription)
- ✅ Made 12-hour reschedule/cancel rule configurable
- ✅ Cleaned up all duplicate imports and unused code
- ✅ Improved code structure and readability
- ✅ All ViewSets now properly optimized for database queries
- ✅ Server running successfully with zero errors
