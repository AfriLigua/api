from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'is_read', 'created_at', 'updated_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants_emails = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants_emails', 'booking', 'last_message', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_participants_emails(self, obj):
        return [p.email for p in obj.participants.all()]
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'sender': last_msg.sender.email,
                'content': last_msg.content[:50],
                'created_at': last_msg.created_at
            }
        return None
