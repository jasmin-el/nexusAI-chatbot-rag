"""URL configuration for the chat application.

This module defines all URL patterns for the RAG chatbot, including
the chat interface, API endpoints for conversation management, and
document upload functionality.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main chat interface (GET: render UI, POST: send message)
    path('', views.chat_view, name='chat'),
    
    # Load specific conversation in chat interface
    path('conversation/<int:conversation_id>/', views.chat_view, name='chat_conversation'),
    
    # API: Get list of all conversations
    path('api/conversations/', views.get_conversations, name='api_conversations'),
    
    # API: Get messages for a specific conversation
    path('api/conversations/<int:conversation_id>/messages/', views.get_messages, name='api_messages'),
    
    # API: Delete a specific conversation
    path('api/conversations/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    
    # Document upload endpoint
    path('upload/', views.upload_document, name='upload_document'),
]
