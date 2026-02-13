import os
from dotenv import load_dotenv

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


settings = BaseSettings()