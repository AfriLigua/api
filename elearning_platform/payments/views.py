from rest_framework import viewsets, permissions
from .models import Payment, TutorWallet, WithdrawalRequest
from .serializers import PaymentSerializer, TutorWalletSerializer, WithdrawalRequestSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.select_related('user', 'booking').all()


class TutorWalletViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TutorWalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TutorWallet.objects.select_related('tutor').all()


class WithdrawalRequestViewSet(viewsets.ModelViewSet):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WithdrawalRequest.objects.select_related('tutor').all()
