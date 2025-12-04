from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('conversation/<int:conversation_id>/', views.chat_view, name='chat_conversation'),
    path('api/conversations/', views.get_conversations, name='api_conversations'),
    path('api/conversations/<int:conversation_id>/messages/', views.get_messages, name='api_messages'),
    path('api/conversations/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('upload/', views.upload_document, name='upload_document'),
]
