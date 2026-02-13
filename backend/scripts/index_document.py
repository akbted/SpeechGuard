import os
import glob
import logging

from src.config.settings import settings, getEmbedding, getVectorStore

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
        return
    
    # Step 2 - Initialize the Embedding Model
    try:
        logger.info("Intializing Embedding Model")
        embeddings = getEmbedding()
        logger.info("Intialized Embedding Model")
    except Exception as e:
        logger.error("Failed to Initialize the embedding due to {e}")
        return
    
    # Step 3 - Initialize the Azure Search
    try:
        logger.info("Intializing Azure Search")
        index_name = getVectorStore(embeddings)
        logger.info("Intialized Azure Search")
    except Exception as e:
        logger.error("Failed to Initialize the Azure Search due to {e}")
        return

    # Step 4 - Find the PDF files in data folder
    get_all_pdfs = os.path.join(data_folder, "*.pdf")
    pdf_files = glob.glob(pathname=get_all_pdfs)
    if not pdf_files:
        logger.warn(f"File Not Found in {data_folder}")
        return 
    
    # Step 5 - Load Each PDF using PyPDF Loader
    


