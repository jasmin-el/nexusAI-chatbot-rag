from django.test import TestCase

# Create your tests here.
from .models import Message

class ChatModelTest(TestCase):
    def test_message_creation(self):
        msg = Message.objects.create(content="Hello")
        self.assertEqual(msg.content, "Hello")