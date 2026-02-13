import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

load_dotenv()

class BaseSettings:
    
    # Storage
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")

    # Azure OpenAi
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION", "")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPEN_AI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPEN_AI_CHAT_DEPLOYMENT", "")

    # Azure Embedding
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "")

    # Azure AI_Search
    AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY", "")
    AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "")

    # Azure Video Indexer
    AZURE_VI_NAME = os.getenv("AZURE_VI_NAME", "")
    AZURE_VI_LOCATION = os.getenv("AZURE_VI_LOCATION", "")
    AZURE_VI_ACCOUNT_ID = os.getenv("AZURE_VI_ACCOUNT_ID", "")
    AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", "")
    AZURE_RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP", "")

    # Azure Monitoring
    APPLICATION_INSIGHT_CONNECTION_STRING = os.getenv("APPLICATION_INSIGHT_CONNECTION_STRING", "")

    # Langsmith Tracking
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "")


    # Data Folder Path
    BACKEND_PATH = Path(__file__).parent.parent.parent
    DATA_FOLDER_PATH = os.path.join(BACKEND_PATH, "data")

def getLLMClient() -> AzureChatOpenAI:
    llm = AzureChatOpenAI(
        azure_deployment=BaseSettings.AZURE_OPEN_AI_CHAT_DEPLOYMENT,
        api_version=BaseSettings.AZURE_OPENAI_VERSION,
        temperature=0.0
    )

def getEmbedding() -> AzureOpenAIEmbeddings:
    embeddings = AzureOpenAIEmbeddings(
        model=BaseSettings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        api_version=BaseSettings.AZURE_OPENAI_VERSION
    )

def getVectorStore(embedding: AzureOpenAIEmbeddings) -> AzureSearch:
    vector_store = AzureSearch(
        azure_search_endpoint=BaseSettings.AZURE_SEARCH_ENDPOINT,
        azure_search_key=BaseSettings.AZURE_SEARCH_API_KEY,
        index_name=BaseSettings.AZURE_SEARCH_INDEX_NAME,
        embedding_function=embedding.embed_query
    )


settings = BaseSettings()