import os
import glob
import logging

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
    
