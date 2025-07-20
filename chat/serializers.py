from rest_framework import serializers
from .models import Thread, Message

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'name', 'participants']

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'thread', 'user', 'content', 'timestamp']
