from rest_framework import serializers
from .models import Payment, TutorWallet, WithdrawalRequest


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['user', 'status', 'transaction_id', 'created_at', 'updated_at']


class TutorWalletSerializer(serializers.ModelSerializer):
    tutor_email = serializers.EmailField(source='tutor.email', read_only=True)
    
    class Meta:
        model = TutorWallet
        fields = '__all__'
        read_only_fields = ['tutor', 'available_balance', 'pending_balance', 'total_earned', 'created_at', 'updated_at']


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    tutor_email = serializers.EmailField(source='tutor.email', read_only=True)
    
    class Meta:
        model = WithdrawalRequest
        fields = '__all__'
        read_only_fields = ['tutor', 'status', 'transaction_id', 'created_at', 'updated_at', 'processed_at']


class WithdrawalRequestCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payout_method = serializers.ChoiceField(choices=WithdrawalRequest.PAYOUT_METHOD_CHOICES)
    payout_details = serializers.JSONField()
