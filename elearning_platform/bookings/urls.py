from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailabilitySlotViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'availability-slots', AvailabilitySlotViewSet, basename='availability-slot')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]
