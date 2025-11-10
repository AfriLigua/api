from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, TutorWalletViewSet, WithdrawalRequestViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'wallets', TutorWalletViewSet)
router.register(r'withdrawals', WithdrawalRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
