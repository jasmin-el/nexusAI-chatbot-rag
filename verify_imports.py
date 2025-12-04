import sys
print(f"Python Executable: {sys.executable}")

try:
    import django
    print(f"SUCCESS: Django {django.get_version()} imported")
except ImportError as e:
    print(f"FAILURE: {e}")

try:
    import langchain_openai
    print("SUCCESS: langchain_openai imported")
except ImportError as e:
    print(f"FAILURE: {e}")

try:
    import pinecone
    print("SUCCESS: pinecone imported")
except ImportError as e:
    print(f"FAILURE: {e}")
