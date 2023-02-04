from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(max_length=500)

