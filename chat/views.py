"""Django views for the RAG Chatbot application.

This module contains all view functions and API endpoints for the chat interface,
including message handling, document upload, and conversation management.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
import os, json
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Conversation, Message
from .rag_service import rag_service


@ensure_csrf_cookie
def chat_view(request, conversation_id=None):
    """Handle chat interface rendering and message processing.
    
    This view serves dual purposes:
    - GET: Renders the chat interface HTML template
    - POST: Processes user messages and returns AI-generated responses
    
    The POST handler also manages conversation creation, title generation,
    and delegates to upload_document() when files are present.
    
    Args:
        request (HttpRequest): Django request object
        conversation_id (int, optional): ID of existing conversation to load
        
    Returns:
        GET: HttpResponse with rendered chat.html template
        POST: JsonResponse with:
            - response (str): AI-generated response text
            - conversation_id (int): ID of the conversation
            
    Raises:
        400 Bad Request: If message is missing in POST body
        500 Internal Server Error: If AI response generation fails
    """
    if request.method == 'POST':
        # Handle file upload
        if request.FILES.get('document'):
            return upload_document(request)
        
        # Handle text message
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            conversation_id = data.get('conversation_id')

            if not user_message:
                return JsonResponse({'error': 'Message is required'}, status=400)

            conversation = None
            if conversation_id:
                try:
                    conversation = Conversation.objects.get(id=conversation_id)
                except Conversation.DoesNotExist:
                    conversation = None

            if not conversation:
                conversation = Conversation.objects.create()

            # Create user message
            Message.objects.create(conversation=conversation, role='user', content=user_message)

            # Update conversation timestamp
            conversation.updated_at = timezone.now()
            # Set title if not exists
            if not conversation.title:
                conversation.title = user_message[:30] + "..." if len(user_message) > 30 else user_message
            conversation.save()

            # Generate AI response
            ai_response_content = rag_service.generate_response(user_message)
            Message.objects.create(conversation=conversation, role='ai', content=ai_response_content)

            # Update timestamp
            conversation.updated_at = timezone.now()
            
            # Generate title if not exists
            if not conversation.title:
                try:
                    title = rag_service.generate_title(user_message, ai_response_content)
                    conversation.title = title
                except Exception as e:
                    print(f"Title generation failed: {e}")
                    # Fallback to first message if generation fails
                    conversation.title = user_message[:30] + "..." if len(user_message) > 30 else user_message
            
            conversation.save()

            return JsonResponse({'response': ai_response_content, 'conversation_id': conversation.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'chat/chat.html', {'initial_conversation_id': conversation_id})


def upload_document(request):
    """Handle document upload and ingestion into RAG knowledge base.
    
    Accepts PDF or TXT files, saves them to media storage, and triggers
    the RAG service to process, embed, and index the document chunks.
    
    Args:
        request (HttpRequest): Django request object with file in FILES
        
    Returns:
        JsonResponse with:
            - message (str): Success message with chunk count
            
    Raises:
        400 Bad Request: If no document provided
        405 Method Not Allowed: If request method is not POST
        500 Internal Server Error: If file processing fails or unsupported file type
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    try:
        uploaded_file = request.FILES.get('document')
        if not uploaded_file:
            return JsonResponse({'error': 'No document provided'}, status=400)
        
        file_path = default_storage.save(f'documents/{uploaded_file.name}', ContentFile(uploaded_file.read()))
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        result_message = rag_service.ingest_file(full_path)
        return JsonResponse({'message': result_message})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_conversations(request):
    """Retrieve list of all conversations ordered by most recent.
    
    Returns all conversations with their metadata, including auto-generated
    titles if not already set. Used to populate the conversation sidebar.
    
    Args:
        request (HttpRequest): Django request object
        
    Returns:
        JsonResponse with:
            - conversations (list): List of conversation objects, each containing:
                - id (int): Conversation ID
                - title (str): Conversation title
                - created_at (str): Creation timestamp (MM/DD HH:MM)
                - updated_at (str): Last update timestamp (MM/DD HH:MM)
    """
    conversations = Conversation.objects.all().order_by('-updated_at')
    data = []

    for c in conversations:
        title = c.title
        if not title:
            first_msg = c.messages.filter(role='user').order_by('created_at').first()
            if first_msg and first_msg.content:
                title = first_msg.content[:30] + "..." if len(first_msg.content) > 30 else first_msg.content
            else:
                title = f"Conversation {c.id}"

        data.append({
            'id': c.id,
            'title': title,
            'created_at': c.created_at.isoformat(),
            'updated_at': c.updated_at.isoformat()
        })

    return JsonResponse({'conversations': data})


def get_messages(request, conversation_id):
    """Retrieve all messages for a specific conversation.
    
    Returns messages in chronological order for display in the chat interface.
    
    Args:
        request (HttpRequest): Django request object
        conversation_id (int): ID of the conversation to retrieve
        
    Returns:
        JsonResponse with:
            - messages (list): List of message objects, each containing:
                - role (str): Either 'user' or 'ai'
                - content (str): Message text content
                - timestamp (str): ISO formatted creation time
                
    Raises:
        404 Not Found: If conversation with given ID doesn't exist
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        messages = conversation.messages.all().order_by('created_at')
        data = [{
            'role': m.role, 
            'content': m.content,
            'timestamp': m.created_at.isoformat()
        } for m in messages]
        return JsonResponse({'messages': data})
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found'}, status=404)


def delete_conversation(request, conversation_id):
    """Delete a conversation and all its associated messages.
    
    Permanently removes a conversation from the database. All messages
    are cascade-deleted due to the foreign key relationship.
    
    Args:
        request (HttpRequest): Django request object
        conversation_id (int): ID of the conversation to delete
        
    Returns:
        JsonResponse with:
            - success (bool): True if deletion succeeded
            
    Raises:
        404 Not Found: If conversation with given ID doesn't exist
        405 Method Not Allowed: If request method is not DELETE
    """
    if request.method == 'DELETE':
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            conversation.delete()
            return JsonResponse({'success': True})
        except Conversation.DoesNotExist:
            return JsonResponse({'error': 'Conversation not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

