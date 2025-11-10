from django.contrib import admin
from .models import Payment, TutorWallet, WithdrawalRequest


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
