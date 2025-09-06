from rest_framework import serializers
from .models import Chat, Message, UserSettings

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = '__all__'

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
