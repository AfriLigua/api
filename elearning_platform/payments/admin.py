from django.contrib import admin
from .models import Payment, TutorWallet, WithdrawalRequest, Transaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'booking', 'amount', 'currency', 'provider', 'status', 'created_at']
    list_filter = ['status', 'provider', 'currency']
    search_fields = ['user__email', 'transaction_id']


@admin.register(TutorWallet)
class TutorWalletAdmin(admin.ModelAdmin):
    list_display = ['tutor', 'available_balance', 'pending_balance', 'total_earned', 'currency']
    search_fields = ['tutor__email']


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'tutor', 'amount', 'status', 'payout_method', 'created_at']
    list_filter = ['status', 'payout_method']
    search_fields = ['tutor__email']
    actions = ['approve_withdrawals']
    
    def approve_withdrawals(self, request, queryset):
        queryset.update(status='approved')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_type', 'user', 'amount', 'commission_rate', 'net_amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'payment_provider']
    search_fields = ['user__email', 'provider_transaction_id']
