# Setup Guide

This guide provides detailed instructions for setting up and configuring the RAG Chatbot application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Azure OpenAI Configuration](#azure-openai-configuration)
- [Pinecone Configuration](#pinecone-configuration)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **MySQL Server**
   - Download from [mysql.com](https://dev.mysql.com/downloads/)
   - Alternative: Use MariaDB or another MySQL-compatible database
   - Verify installation: `mysql --version`

3. **pip** (Python package manager)
   - Usually comes with Python
   - Verify installation: `pip --version`

### Required Accounts

1. **Azure OpenAI Account**
   - Sign up at [Azure Portal](https://portal.azure.com/)
   - Request access to Azure OpenAI Service
   - Create a resource and deploy models

2. **Pinecone Account**
   - Sign up at [pinecone.io](https://www.pinecone.io/)
   - Free tier available for development

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd RAG-CHATBOT
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install MySQL Client (if needed)

**Windows:**
```bash
pip install mysqlclient
```

**macOS:**
```bash
brew install mysql
pip install mysqlclient
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

## Environment Configuration

### 1. Create .env File

Create a `.env` file in the project root directory:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

If `.env.example` doesn't exist, create `.env` manually with the following template:

### 2. Configure Environment Variables

```env
# ============================================
# Azure OpenAI Configuration
# ============================================
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_CHAT_DEPLOYMENT=your-gpt-deployment-name
AZURE_EMBEDDING_DEPLOYMENT=your-embedding-deployment-name

# ============================================
# Pinecone Configuration
# ============================================
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=rag-chatbot-index
PINECONE_HOST=your-index-id.svc.environment.pinecone.io

# ============================================
# Database Configuration
# ============================================
DB_NAME=rag_chatbot
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

> [!IMPORTANT]
> Never commit the `.env` file to version control. It's already included in `.gitignore`.

## Database Setup

### 1. Create MySQL Database

Connect to MySQL:

```bash
mysql -u root -p
```

Create the database:

```sql
CREATE DATABASE rag_chatbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 2. Update Database Credentials

Update the database configuration in your `.env` file:

```env
DB_NAME=rag_chatbot
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

### 3. Run Migrations

Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the following tables:
- `chat_conversation`: Stores conversation metadata
- `chat_message`: Stores individual messages
- `chat_document`: Stores uploaded document metadata

### 4. Create Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

## Azure OpenAI Configuration

### 1. Create Azure OpenAI Resource

1. Go to [Azure Portal](https://portal.azure.com/)
2. Click **Create a resource**
3. Search for **Azure OpenAI**
4. Click **Create** and fill in:
   - Subscription
   - Resource group
   - Region
   - Name
   - Pricing tier

### 2. Deploy Chat Model

1. Navigate to your Azure OpenAI resource
2. Go to **Model deployments** → **Manage Deployments**
3. Click **Create new deployment**
4. Select a model:
   - **Recommended**: `gpt-4` or `gpt-35-turbo`
5. Give it a deployment name (e.g., `gpt-4-chat`)
6. Click **Create**

### 3. Deploy Embedding Model

1. Click **Create new deployment** again
2. Select an embedding model:
   - **Recommended**: `text-embedding-3-small`
3. Give it a deployment name (e.g., `text-embedding-3-small`)
4. **Important**: Set dimensions to **1024**
5. Click **Create**

### 4. Get API Credentials

1. Go to **Keys and Endpoint** in your Azure OpenAI resource
2. Copy:
   - **Endpoint** (e.g., `https://your-resource.openai.azure.com/`)
   - **Key 1** or **Key 2**

### 5. Update .env File

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_CHAT_DEPLOYMENT=gpt-4-chat
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

> [!WARNING]
> The embedding model **must** output 1024-dimensional vectors to match the Pinecone index configuration in `rag_service.py`.

## Pinecone Configuration

### 1. Create Pinecone Account

1. Sign up at [pinecone.io](https://www.pinecone.io/)
2. Verify your email
3. Log in to the Pinecone console

### 2. Create Serverless Index

1. Click **Create Index**
2. Configure the index:
   - **Name**: `rag-chatbot-index` (or your preferred name)
   - **Dimensions**: **1024** (must match embedding model)
   - **Metric**: **Cosine**
   - **Index Type**: **Serverless**
   - **Cloud Provider**: Choose your preferred provider
   - **Region**: Choose a region close to your application

3. Click **Create Index**

### 3. Get API Credentials

1. Go to **API Keys** in the Pinecone console
2. Copy your API key
3. Go to your index and copy the **Host** URL
   - Format: `your-index-id.svc.environment.pinecone.io`

### 4. Update .env File

```env
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=rag-chatbot-index
PINECONE_HOST=your-index-id.svc.environment.pinecone.io
```

> [!NOTE]
> The Pinecone host URL can be found in the index details page. Make sure to include the full host without `https://`.

## Running the Application

### 1. Verify Configuration

Test that all dependencies are installed:

```bash
python verify_imports.py
```

### 2. Start Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

### 3. Access the Application

Open your browser and navigate to:

```
http://localhost:8000/chat/
```

### 4. Test the Chat Interface

1. Upload a document (PDF or TXT)
2. Wait for processing confirmation
3. Ask questions about the document
4. Verify responses are contextually relevant

## Troubleshooting

### Database Connection Issues

**Error**: `django.db.utils.OperationalError: (2002, "Can't connect to MySQL server")`

**Solutions**:
- Ensure MySQL server is running: `sudo service mysql start` (Linux) or check Services (Windows)
- Verify database credentials in `.env`
- Check that the database exists: `mysql -u root -p -e "SHOW DATABASES;"`
- Ensure `DB_HOST` and `DB_PORT` are correct

### Azure OpenAI API Errors

**Error**: `AuthenticationError` or `InvalidRequestError`

**Solutions**:
- Verify `AZURE_OPENAI_API_KEY` is correct
- Check `AZURE_OPENAI_ENDPOINT` format (should end with `/`)
- Ensure deployment names match exactly (case-sensitive)
- Verify API version is supported: `2024-02-15-preview`
- Check Azure OpenAI resource is active and not suspended

**Error**: `DeploymentNotFound`

**Solutions**:
- Verify deployment names in Azure Portal
- Ensure deployments are fully created and active
- Check for typos in `.env` file

### Pinecone Connection Issues

**Error**: `PineconeException` or connection timeout

**Solutions**:
- Verify `PINECONE_API_KEY` is correct
- Check `PINECONE_HOST` format (no `https://` prefix)
- Ensure index exists and is active
- Verify index dimensions are 1024
- Check network connectivity to Pinecone

**Error**: `Dimension mismatch`

**Solutions**:
- Ensure Pinecone index has 1024 dimensions
- Verify Azure embedding model outputs 1024-dimensional vectors
- Check `dimensions=1024` in `rag_service.py` line 35

### Document Upload Issues

**Error**: `FileNotFoundError` or permission denied

**Solutions**:
- Ensure `media/` directory exists: `mkdir media`
- Check directory permissions: `chmod 755 media`
- Verify `MEDIA_ROOT` in `settings.py` points to correct path

**Error**: `Unsupported file type`

**Solutions**:
- Only PDF and TXT files are supported
- Check file extension is lowercase
- Verify file is not corrupted

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'X'`

**Solutions**:
- Reinstall dependencies: `pip install -r requirements.txt`
- Ensure virtual environment is activated
- For `mysqlclient` issues, install system dependencies (see Installation section)

### Migration Issues

**Error**: `django.db.migrations.exceptions.InconsistentMigrationHistory`

**Solutions**:
- Delete migration files (except `__init__.py`) in `chat/migrations/`
- Drop and recreate database
- Run `python manage.py makemigrations` and `python manage.py migrate`

## Next Steps

- Read [API.md](API.md) for API endpoint documentation
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system architecture details
- Explore the chat interface and test different queries
- Upload your own documents and build a custom knowledge base

## Getting Help

If you encounter issues not covered here:

1. Check the [README.md](README.md) troubleshooting section
2. Review error logs in the terminal
3. Enable Django debug mode and check detailed error pages
4. Open an issue on the GitHub repository

---

**Happy chatting! 🚀**
