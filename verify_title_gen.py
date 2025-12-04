import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_chatbot.settings')
django.setup()

from chat.rag_service import rag_service

def test_title_generation():
    print("Testing title generation...")
    user_msg = "What is Azure?"
    ai_msg = "Azure is Microsoft's cloud computing platform."
    
    try:
        title = rag_service.generate_title(user_msg, ai_msg)
        print(f"Success! Generated title: '{title}'")
    except Exception as e:
        print(f"Error generating title: {e}")

if __name__ == "__main__":
    test_title_generation()
