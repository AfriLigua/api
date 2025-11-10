from rest_framework import serializers
from .models import AvailabilitySlot, Booking


class AvailabilitySlotSerializer(serializers.ModelSerializer):
    tutor_email = serializers.EmailField(source='tutor.email', read_only=True)
    duration_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = AvailabilitySlot
        fields = '__all__'
        read_only_fields = ['is_booked', 'created_at', 'updated_at', 'tutor']
    
    def get_duration_minutes(self, obj):
        return obj.get_duration_minutes()


class BookingSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)
    tutor_email = serializers.EmailField(source='tutor.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    slot_start = serializers.DateTimeField(source='availability_slot.start_time', read_only=True)
    slot_end = serializers.DateTimeField(source='availability_slot.end_time', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['student', 'tutor', 'status', 'platform_fee', 'tutor_earnings', 'created_at', 'updated_at']


class BookingCreateSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    availability_slot_id = serializers.IntegerField()
