"""Django models for the RAG Chatbot application.

This module defines the database schema for conversations, messages, and documents.
The models support a chat interface with conversation history and document upload
functionality for the RAG (Retrieval-Augmented Generation) pipeline.
"""

from django.db import models


class Conversation(models.Model):
    """Represents a chat conversation with message history.
    
    A conversation groups related messages together and maintains metadata
    like creation time and auto-generated title. Conversations are ordered
    by most recently updated for display in the sidebar.
    
    Attributes:
        created_at (datetime): Timestamp when conversation was created
        title (str): Auto-generated or custom conversation title (max 255 chars)
        updated_at (datetime): Timestamp of last activity in conversation
    """
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """Return string representation of the conversation.
        
        Returns:
            str: Formatted string with conversation ID and creation date
        """
        return f"Conversation {self.id} - {self.created_at}"


class Message(models.Model):
    """Represents a single message in a conversation.
    
    Messages can be from either the user or the AI assistant. Each message
    is linked to a conversation and stored with its content and timestamp.
    
    Attributes:
        conversation (ForeignKey): Reference to parent Conversation
        role (str): Either 'user' or 'ai' indicating message sender
        content (str): The actual message text content
        created_at (datetime): Timestamp when message was created
    """
    ROLE_CHOICES = (
        ('user', 'User'),
        ('ai', 'AI'),
    )
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the message.
        
        Returns:
            str: Role and first 50 characters of content
        """
        return f"{self.role}: {self.content[:50]}..."


class Document(models.Model):
    """Represents an uploaded document for RAG knowledge base.
    
    Documents are uploaded by users and processed into embeddings for
    retrieval-augmented generation. Supports PDF and TXT file formats.
    
    Attributes:
        title (str): Document title (max 255 chars)
        file_path (str): Path to uploaded file in media storage
        uploaded_at (datetime): Timestamp when document was uploaded
        processed (bool): Whether document has been embedded and indexed
    """
    title = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1024)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        """Return string representation of the document.
        
        Returns:
            str: Document title
        """
        return self.title
