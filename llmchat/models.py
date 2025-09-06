from django.db import models
from django.contrib.auth.models import User
import json

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # 'user' or 'assistant'
    content = models.TextField()
    model = models.CharField(max_length=100, null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)
    usage = models.JSONField(null=True, blank=True)  # Store token usage
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}"

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    settings = models.JSONField(default=dict)  # Store all settings as JSON
    
    def __str__(self):
        return f"Settings for {self.user.username}"