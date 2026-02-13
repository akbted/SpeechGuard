import os
import glob
import logging

from src.config.settings import settings, getEmbedding

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name="Azure Document Indexer")

def index_docs():
    """
    Read PDFs,
    Chunk Documents,
    Upload Document Azure
    """

    # Step 1 - Find the data folder path
    data_folder = settings.DATA_FOLDER_PATH
    if not data_folder:
        raise Exception("Data Folder Not Found - give the correct path")
    
    # Step 2 - Initialize the Embedding Model
    try:
        logger.info("Intializing Embedding Model")
        embeddings = getEmbedding()
    except Exception as e:
        logger.error("Failed to Initialize the embedding due to {e}")
    
    # Step 3 -Initialize the Azure Search

