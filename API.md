# API Documentation

This document provides detailed information about the RAG Chatbot API endpoints.

## Base URL

```
http://localhost:8000/chat/
```

## Authentication

The API uses Django's CSRF protection for POST requests. When making requests from the frontend, ensure you include the CSRF token in your request headers.

## Endpoints

### 1. Chat Interface

#### GET `/chat/`

Renders the main chat interface.

**Response**: HTML page with chat UI

**Example**:
```
GET http://localhost:8000/chat/
```

---

### 2. Load Conversation

#### GET `/chat/conversation/<conversation_id>/`

Loads a specific conversation in the chat interface.

**Parameters**:
- `conversation_id` (path parameter): Integer ID of the conversation

**Response**: HTML page with chat UI and loaded conversation

**Example**:
```
GET http://localhost:8000/chat/conversation/5/
```

---

### 3. Send Message

#### POST `/chat/`

Sends a message and receives an AI response.

**Request Headers**:
```
Content-Type: application/json
X-CSRFToken: <csrf-token>
```

**Request Body**:
```json
{
  "message": "What is machine learning?",
  "conversation_id": 5
}
```

**Parameters**:
- `message` (string, required): The user's message
- `conversation_id` (integer, optional): ID of existing conversation. If omitted, a new conversation is created.

**Response** (200 OK):
```json
{
  "response": "Machine learning is a subset of artificial intelligence...",
  "conversation_id": 5
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Message is required"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "error": "Error message details"
}
```

**Example**:
```javascript
fetch('/chat/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify({
    message: 'What is machine learning?',
    conversation_id: 5
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 4. Upload Document

#### POST `/chat/upload/`

Uploads a document to be processed and added to the knowledge base.

**Request Headers**:
```
Content-Type: multipart/form-data
X-CSRFToken: <csrf-token>
```

**Request Body** (FormData):
- `document` (file): PDF or TXT file to upload

**Response** (200 OK):
```json
{
  "message": "Ingested 42 chunks from document.pdf"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "No document provided"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "error": "Unsupported file type"
}
```

**Supported File Types**:
- PDF (`.pdf`)
- Text (`.txt`)

**Example**:
```javascript
const formData = new FormData();
formData.append('document', fileInput.files[0]);

fetch('/chat/upload/', {
  method: 'POST',
  headers: {
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 5. Get Conversations

#### GET `/chat/api/conversations/`

Retrieves a list of all conversations, ordered by most recently updated.

**Response** (200 OK):
```json
{
  "conversations": [
    {
      "id": 5,
      "title": "Machine Learning Discussion",
      "created_at": "12/04 10:30",
      "updated_at": "12/04 10:35"
    },
    {
      "id": 4,
      "title": "Python Programming",
      "created_at": "12/03 14:20",
      "updated_at": "12/03 15:10"
    }
  ]
}
```

**Response Fields**:
- `id` (integer): Conversation ID
- `title` (string): Conversation title (auto-generated or from first message)
- `created_at` (string): Creation timestamp (format: `MM/DD HH:MM`)
- `updated_at` (string): Last update timestamp (format: `MM/DD HH:MM`)

**Example**:
```javascript
fetch('/chat/api/conversations/')
  .then(response => response.json())
  .then(data => console.log(data.conversations));
```

---

### 6. Get Messages

#### GET `/chat/api/conversations/<conversation_id>/messages/`

Retrieves all messages in a specific conversation.

**Parameters**:
- `conversation_id` (path parameter): Integer ID of the conversation

**Response** (200 OK):
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is machine learning?"
    },
    {
      "role": "ai",
      "content": "Machine learning is a subset of artificial intelligence..."
    },
    {
      "role": "user",
      "content": "Can you give me an example?"
    },
    {
      "role": "ai",
      "content": "Sure! A common example is email spam filtering..."
    }
  ]
}
```

**Response Fields**:
- `role` (string): Either `"user"` or `"ai"`
- `content` (string): Message content

**Error Response** (404 Not Found):
```json
{
  "error": "Conversation not found"
}
```

**Example**:
```javascript
fetch('/chat/api/conversations/5/messages/')
  .then(response => response.json())
  .then(data => console.log(data.messages));
```

---

### 7. Delete Conversation

#### DELETE `/chat/api/conversations/<conversation_id>/delete/`

Deletes a conversation and all its messages.

**Parameters**:
- `conversation_id` (path parameter): Integer ID of the conversation

**Request Headers**:
```
X-CSRFToken: <csrf-token>
```

**Response** (200 OK):
```json
{
  "success": true
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Conversation not found"
}
```

**Error Response** (405 Method Not Allowed):
```json
{
  "error": "Method not allowed"
}
```

**Example**:
```javascript
fetch('/chat/api/conversations/5/delete/', {
  method: 'DELETE',
  headers: {
    'X-CSRFToken': getCookie('csrftoken')
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Data Models

### Conversation

```python
{
  "id": int,
  "title": str,
  "created_at": datetime,
  "updated_at": datetime
}
```

### Message

```python
{
  "id": int,
  "conversation_id": int,
  "role": str,  # "user" or "ai"
  "content": str,
  "created_at": datetime
}
```

### Document

```python
{
  "id": int,
  "title": str,
  "file_path": str,
  "uploaded_at": datetime,
  "processed": bool
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: HTTP method not supported
- `500 Internal Server Error`: Server error

Error responses include a JSON object with an `error` field:

```json
{
  "error": "Descriptive error message"
}
```

---

## CSRF Protection

Django's CSRF protection is enabled. For POST, PUT, PATCH, and DELETE requests, include the CSRF token:

**JavaScript Helper**:
```javascript
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
```

**Usage**:
```javascript
headers: {
  'X-CSRFToken': getCookie('csrftoken')
}
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider implementing rate limiting using:
- Django Ratelimit
- Django REST Framework throttling
- Nginx rate limiting

---

## Examples

### Complete Chat Flow

```javascript
// 1. Start a new conversation
fetch('/chat/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify({
    message: 'Hello, what can you help me with?'
  })
})
.then(response => response.json())
.then(data => {
  console.log('AI Response:', data.response);
  const conversationId = data.conversation_id;
  
  // 2. Continue the conversation
  return fetch('/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      message: 'Tell me about machine learning',
      conversation_id: conversationId
    })
  });
})
.then(response => response.json())
.then(data => {
  console.log('AI Response:', data.response);
});
```

### Upload and Query Document

```javascript
// 1. Upload a document
const formData = new FormData();
formData.append('document', fileInput.files[0]);

fetch('/chat/upload/', {
  method: 'POST',
  headers: {
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log(data.message);
  
  // 2. Ask a question about the document
  return fetch('/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      message: 'What are the main points in this document?'
    })
  });
})
.then(response => response.json())
.then(data => {
  console.log('AI Response:', data.response);
});
```

---

## Best Practices

1. **Always include CSRF tokens** for state-changing requests
2. **Handle errors gracefully** with try-catch blocks
3. **Validate user input** before sending to the API
4. **Show loading states** during API calls
5. **Implement retry logic** for failed requests
6. **Cache conversation lists** to reduce API calls
7. **Debounce rapid requests** to avoid overwhelming the server

---

For more information about the system architecture, see [ARCHITECTURE.md](ARCHITECTURE.md).
