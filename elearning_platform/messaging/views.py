from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.select_related('booking').prefetch_related('participants').all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.select_related('sender', 'conversation').all()
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
