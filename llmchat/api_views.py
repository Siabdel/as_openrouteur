from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Chat, Message, UserSettings
from .serializers import ChatSerializer, MessageSerializer, UserSettingsSerializer

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    
    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(chat__user=self.request.user)

class UserSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSettingsSerializer
    
    def get_queryset(self):
        return UserSettings.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Ensure user has only one settings object
        settings, created = UserSettings.objects.get_or_create(
            user=request.user,
            defaults={'settings': request.data.get('settings', {})}
        )
        if not created:
            settings.settings = request.data.get('settings', {})
            settings.save()
        
        serializer = self.get_serializer(settings)
        return Response(serializer.data, status=status.HTTP_200_OK)