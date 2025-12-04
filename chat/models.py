from django.db import models

class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Conversation {self.id} - {self.created_at}"

class Message(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('ai', 'AI'),
    )
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."

class Document(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1024)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
