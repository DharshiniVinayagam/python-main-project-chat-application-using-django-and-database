from django.db import models

class ChatMessage(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.message[:50]}"
