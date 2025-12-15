from django.test import TestCase

# Create your tests here.
import os
import django
import json
# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_chatbot.settings')
django.setup()

from django.test import RequestFactory
from chat.views import get_conversations, get_messages
from chat.models import Conversation, Message

def test():
    print("Testing Chat APIs...")
    factory = RequestFactory()

    # 1. Create a dummy conversation
    conv = Conversation.objects.create(title="Test Conversation")
    Message.objects.create(conversation=conv, role='user', content="Hello")
    Message.objects.create(conversation=conv, role='ai', content="Hi there!")
    print(f"Created conversation: {conv.id}")

    # 2. Test get_conversations
    request = factory.get('/chat/api/conversations/')
    response = get_conversations(request)
    data = json.loads(response.content)
    print(f"get_conversations response: {len(data['conversations'])} conversations found.")
    assert len(data['conversations']) > 0
    assert data['conversations'][0]['title'] == "Test Conversation" or "Conversation" in data['conversations'][0]['title']

    # 3. Test get_messages
    request = factory.get(f'/chat/api/conversations/{conv.id}/messages/')
    response = get_messages(request, conv.id)
    data = json.loads(response.content)
    print(f"get_messages response: {len(data['messages'])} messages found.")
    assert len(data['messages']) == 2
    assert data['messages'][0]['content'] == "Hello"

    print("All API tests passed!")

if __name__ == "__main__":
    test()
