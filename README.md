# 🎓 afriligua- E-Learning & Tutor Booking Backend

A powerful and scalable backend built with **Django REST Framework**, designed for an **online language e-learning and tutor booking platform**.  
It supports **tutor-student matching, payments (Wise, PayPal, Credit Card)**, **automated earnings distribution**, **real-time messaging**, and **email + in-app notifications**.

---

## 🚀 Features

### 🧠 Core Modules
- **User Management**
  - Role-based authentication (Admin, Tutor, Student)
  - JWT Authentication (Login, Registration, Password Reset)
  - Profile management with avatar upload

- **Tutor Management**
  - Tutors can set hourly lesson rates
  - Tutors select courses they want to teach
  - Tutors can view their earnings and payment history
  - Featured tutors displayed on home page (based on rating/reviews)

- **Student Management**
  - Students can search and book tutors
  - Manage enrolled courses and booking history
  - Leave reviews/testimonials after sessions

- **Courses**
  - CRUD operations for course categories and lessons
  - Tutor-course linking for specialization
  - Student progress tracking (optional)

- **Messaging System**
  - Secure tutor-student chat limited to booked pairs
  - Real-time communication (via WebSockets or REST polling)

- **Notifications**
  - In-app and email notifications for:
    - New booking confirmations
    - Lesson reminders
    - Payment success/failure
    - Tutor payout completed
  - Email templates included for all notifications

- **Payments**
  - Integrated with **Wise**, **PayPal**, and **Credit Card (Stripe optional)**
  - Students pay at booking
  - Admin holds funds in escrow
  - After lesson completion:
    - 85% goes to tutor (after 15% platform fee)
    - Automated payout to tutor via Wise API
  - Transaction logging and payment history endpoints

- **Reviews & Testimonials**
  - Students can rate tutors
  - Featured tutors automatically selected by rating and performance

- **Admin Dashboard**
  - Manage users, bookings, payments, notifications
  - Approve or suspend tutors
  - View analytics on courses and earnings

---

## 🏗️ Tech Stack

| Component | Technology |
|------------|-------------|
| Framework | Django 5 + Django REST Framework |
| Database | PostgreSQL |
| Authentication | JWT (SimpleJWT) |
| Payments | Wise API, PayPal REST API |
| Notifications | Django Channels (for in-app) + SMTP/SendGrid (for emails) |
| Storage | AWS S3 / Cloudinary for media |
| API Docs | Swagger + Redoc |
| Deployment | Render / Replit / Docker-ready setup |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ateso-learn-backend.git
cd ateso-learn-backend

