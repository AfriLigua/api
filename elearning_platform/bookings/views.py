from rest_framework import viewsets, permissions
from .models import AvailabilitySlot, Booking
from .serializers import AvailabilitySlotSerializer, BookingSerializer


class AvailabilitySlotViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AvailabilitySlot.objects.select_related('tutor').all()
    
    def perform_create(self, serializer):
        serializer.save(tutor=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.select_related(
            'student', 'tutor', 'course', 'availability_slot', 'subscription'
        ).all()
