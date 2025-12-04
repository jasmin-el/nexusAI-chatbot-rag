from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self):
        # Azure OpenAI Configuration
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.azure_embedding_deployment = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
        self.azure_chat_deployment = os.getenv("AZURE_CHAT_DEPLOYMENT")
        
        # Pinecone Configuration
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.pinecone_host = os.getenv("PINECONE_HOST")

        # --- Pinecone client (v3 for serverless) ---
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index = self.pc.Index(self.index_name, host=self.pinecone_host)

        # --- Azure OpenAI Embeddings + LLM ---
        self.embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=self.azure_endpoint,
            api_key=self.azure_api_key,
            api_version=self.azure_api_version,
            azure_deployment=self.azure_embedding_deployment,
            dimensions=1024
        )
        
        self.llm = AzureChatOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.azure_api_key,
            api_version=self.azure_api_version,
            azure_deployment=self.azure_chat_deployment,
            temperature=0.7
        )

    def ingest_file(self, file_path):
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)

        # Add to Pinecone directly
        import hashlib
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = self.embeddings.embed_query(chunk.page_content)
            # Create ASCII-safe ID using MD5 hash of filename + index
            file_id = hashlib.md5(os.path.basename(file_path).encode('utf-8')).hexdigest()
            vector_id = f"{file_id}-{i}"
            
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "text": chunk.page_content,
                    "source": os.path.basename(file_path)
                }
            })
        
        self.index.upsert(vectors=vectors)
        return f"Ingested {len(chunks)} chunks from {os.path.basename(file_path)}"

    def generate_response(self, query):
        # Get embedding for query
        query_embedding = self.embeddings.embed_query(query)
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=3,
            include_metadata=True
        )

        if not results['matches']:
            return "No documents ingested yet."

        # Extract context from results
        context = "\n\n".join([match['metadata']['text'] for match in results['matches']])
        
        messages = [
            SystemMessage(content=(
                "Tu es un assistant professionnel et précis. "
                "Réponds de manière claire, structurée et complète, uniquement en texte simple. "
                "Ne mets pas de gras, pas de titres en Markdown, pas d'étoiles, ni de symboles spéciaux. "
                "Chaque fois que tu utilises un tiret pour lister des éléments, commence une nouvelle ligne après le tiret. "
                "Utilise des paragraphes et phrases lisibles pour un style professionnel."
            )),
            HumanMessage(content=f"Contexte:\n{context}\n\nQuestion: {query}")
        ]

        response = self.llm.invoke(messages)
        return response.content

    def generate_title(self, user_message, ai_response):
        messages = [
            SystemMessage(content="Tu es un expert en synthèse. Génère un titre très court (max 5-6 mots) et professionnel pour cette conversation. Ne mets pas de guillemets, pas de point final."),
            HumanMessage(content=f"Message utilisateur: {user_message}\nRéponse AI: {ai_response}\n\nTitre:")
        ]
        response = self.llm.invoke(messages)
        return response.content.strip()

# Singleton
rag_service = RAGService()
