from rest_framework import generics, permissions
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        recipient_id = self.request.query_params.get('recipient')
        
        if recipient_id:
            # Chat history between current user and specific recipient
            return Message.objects.filter(
                Q(sender=user, recipient_id=recipient_id) | 
                Q(sender_id=recipient_id, recipient=user)
            ).order_by('timestamp')
        
        # Default: all messages involving the user (maybe conversation list?)
        # For simplicity, let's just return all messages for the user
        return Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
