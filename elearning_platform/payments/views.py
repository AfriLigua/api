from rest_framework import viewsets, permissions
from .models import Payment, TutorWallet, WithdrawalRequest
from .serializers import PaymentSerializer, TutorWalletSerializer, WithdrawalRequestSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TutorWalletViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TutorWallet.objects.all()
    serializer_class = TutorWalletSerializer
    permission_classes = [permissions.IsAuthenticated]


class WithdrawalRequestViewSet(viewsets.ModelViewSet):
    queryset = WithdrawalRequest.objects.all()
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
