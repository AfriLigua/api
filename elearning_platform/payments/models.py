from django.db import models
from django.conf import settings
from django.utils import timezone


class Payment(models.Model):
    PROVIDER_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('wise', 'Wise'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='stripe')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment #{self.id} - {self.amount} {self.currency} - {self.status}"


class TutorWallet(models.Model):
    tutor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    available_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pending_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tutor_wallets'
        verbose_name = 'Tutor Wallet'
        verbose_name_plural = 'Tutor Wallets'
    
    def __str__(self):
        return f"{self.tutor.email} - Wallet"
    
    def add_earnings(self, amount, is_pending=True):
        if is_pending:
            self.pending_balance += amount
        else:
            self.available_balance += amount
        self.total_earned += amount
        self.save()
    
    def release_pending_to_available(self, amount):
        if self.pending_balance >= amount:
            self.pending_balance -= amount
            self.available_balance += amount
            self.save()
            return True
        return False
    
    def withdraw(self, amount):
        if self.available_balance >= amount:
            self.available_balance -= amount
            self.save()
            return True
        return False


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )
    
    PAYOUT_METHOD_CHOICES = (
        ('paypal', 'PayPal'),
        ('wise', 'Wise'),
        ('payoneer', 'Payoneer'),
        ('skrill', 'Skrill'),
        ('bank_transfer', 'Bank Transfer'),
    )
    
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='withdrawal_requests'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payout_method = models.CharField(max_length=20, choices=PAYOUT_METHOD_CHOICES, default='paypal')
    payout_details = models.JSONField(help_text='Payment details like email, account number, etc.')
    admin_notes = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'withdrawal_requests'
        verbose_name = 'Withdrawal Request'
        verbose_name_plural = 'Withdrawal Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Withdrawal #{self.id} - {self.tutor.email} - {self.amount} {self.currency}"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('lesson_payment', 'Lesson Payment'),
        ('subscription_payment', 'Subscription Payment'),
        ('tutor_payout', 'Tutor Payout'),
        ('refund', 'Refund'),
        ('commission', 'Platform Commission'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('reversed', 'Reversed'),
    )
    
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPE_CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        related_name='transactions',
        blank=True,
        null=True
    )
    subscription = models.ForeignKey(
        'bookings.Subscription',
        on_delete=models.SET_NULL,
        related_name='transactions',
        blank=True,
        null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Commission rate as percentage')
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text='Amount after commission')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_provider = models.CharField(max_length=50, blank=True)
    provider_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Transaction #{self.id} - {self.transaction_type} - {self.amount} {self.currency}"
    
    def calculate_commission(self, commission_rate):
        self.commission_rate = commission_rate * 100
        self.commission_amount = self.amount * commission_rate
        self.net_amount = self.amount - self.commission_amount
        self.save()
    
    def mark_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
