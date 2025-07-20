from rest_framework import generics, permissions
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer

class ThreadListCreateView(generics.ListCreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        return Message.objects.filter(thread_id=thread_id).order_by('timestamp')

    def perform_create(self, serializer):
        thread_id = self.kwargs['thread_id']
        serializer.save(user=self.request.user, thread_id=thread_id)
