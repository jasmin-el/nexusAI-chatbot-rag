# RAG Chatbot

A powerful Retrieval-Augmented Generation (RAG) chatbot built with Django, Azure OpenAI, and Pinecone. This application enables intelligent conversations powered by your own documents, combining the capabilities of large language models with custom knowledge retrieval.

## 🌟 Features

- **💬 Intelligent Conversations**: Chat with an AI assistant powered by Azure OpenAI's GPT models
- **📄 Document Upload**: Upload PDF and text documents to create a custom knowledge base
- **🔍 RAG Pipeline**: Retrieval-Augmented Generation for accurate, context-aware responses
- **💾 Conversation Management**: Save, load, and delete conversation history
- **🎯 Smart Title Generation**: Automatic conversation title generation using GPT
- **🗂️ Vector Storage**: Efficient document embedding and retrieval with Pinecone
- **🎨 Modern UI**: Clean, responsive chat interface

## 🛠️ Technology Stack

### Backend
- **Django 4.0+**: Web framework
- **MySQL**: Database for conversation and message storage
- **Python 3.8+**: Programming language

### AI & ML
- **Azure OpenAI**: GPT models for chat and embeddings
- **LangChain**: Framework for building RAG applications
- **Pinecone**: Serverless vector database for document embeddings

### Document Processing
- **PyPDF**: PDF document parsing
- **LangChain Text Splitters**: Intelligent document chunking

## 📋 Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher
- MySQL database server
- Azure OpenAI account with:
  - Chat deployment (e.g., GPT-4 or GPT-3.5)
  - Embedding deployment (e.g., text-embedding-3-small)
- Pinecone account with a serverless index

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd RAG-CHATBOT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_CHAT_DEPLOYMENT=your-chat-deployment-name
AZURE_EMBEDDING_DEPLOYMENT=your-embedding-deployment-name

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=your-index-name
PINECONE_HOST=your-index-host.pinecone.io

# Database Configuration
DB_NAME=rag_chatbot
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

### 4. Set Up Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/chat/` to start chatting!

## 📁 Project Structure

```
RAG-CHATBOT/
├── chat/                      # Main Django app
│   ├── models.py             # Database models (Conversation, Message, Document)
│   ├── views.py              # API endpoints and view logic
│   ├── rag_service.py        # RAG pipeline implementation
│   ├── urls.py               # URL routing
│   └── templates/            # HTML templates
│       └── chat/
│           └── chat.html     # Chat interface
├── rag_chatbot/              # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
├── media/                    # Uploaded documents storage
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (create this)
```

## 🎯 Usage

### Uploading Documents

1. Click the **Upload Document** button in the chat interface
2. Select a PDF or TXT file
3. Wait for the document to be processed and embedded
4. Start asking questions about your documents!

### Chatting

1. Type your message in the input field
2. Press Enter or click Send
3. The AI will retrieve relevant context from your documents and generate a response

### Managing Conversations

- **New Chat**: Click the "New Chat" button to start a fresh conversation
- **Load Conversation**: Click on any conversation in the sidebar to load it
- **Delete Conversation**: Click the delete icon next to a conversation

## 🔧 Configuration

### Azure OpenAI Setup

1. Create an Azure OpenAI resource in the Azure Portal
2. Deploy a chat model (e.g., `gpt-4`, `gpt-35-turbo`)
3. Deploy an embedding model (e.g., `text-embedding-3-small` with 1024 dimensions)
4. Copy the endpoint, API key, and deployment names to your `.env` file

### Pinecone Setup

1. Create a free account at [Pinecone](https://www.pinecone.io/)
2. Create a serverless index with:
   - **Dimensions**: 1024 (must match your embedding model)
   - **Metric**: Cosine similarity
3. Copy the API key and index host to your `.env` file

### Database Setup

The project uses MySQL by default. To use a different database:

1. Install the appropriate database driver
2. Update the `DATABASES` configuration in `rag_chatbot/settings.py`

## 📚 API Documentation

For detailed API endpoint documentation, see [API.md](API.md).

## 🏗️ Architecture

For a detailed explanation of the system architecture and design decisions, see [ARCHITECTURE.md](ARCHITECTURE.md).

## 🔍 How It Works

1. **Document Ingestion**: Documents are uploaded, split into chunks, and embedded using Azure OpenAI embeddings
2. **Vector Storage**: Embeddings are stored in Pinecone for efficient similarity search
3. **Query Processing**: User questions are embedded and used to retrieve relevant document chunks
4. **Response Generation**: Retrieved context is combined with the user's question and sent to GPT for answer generation
5. **Conversation Management**: All messages are stored in MySQL for conversation history

## 🧪 Testing

The project includes verification scripts:

- `verify_imports.py`: Check if all dependencies are installed
- `verify_chat_api.py`: Test the chat API endpoint
- `verify_title_gen.py`: Verify title generation functionality

Run tests with:

```bash
python verify_imports.py
python verify_chat_api.py
python verify_title_gen.py
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Ensure MySQL is running
- Verify database credentials in `.env`
- Check that the database exists

**Azure OpenAI API Error**
- Verify your API key and endpoint
- Check deployment names match your Azure resources
- Ensure API version is compatible

**Pinecone Connection Error**
- Verify API key and index name
- Ensure index dimensions match embedding model (1024)
- Check that the host URL is correct

**Document Upload Fails**
- Ensure `MEDIA_ROOT` directory exists and is writable
- Check file format (only PDF and TXT supported)
- Verify file size is reasonable

For detailed setup instructions, see [SETUP.md](SETUP.md).

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

**Built with ❤️ using Django, Azure OpenAI, and Pinecone**
