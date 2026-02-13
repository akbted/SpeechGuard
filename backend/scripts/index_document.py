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
        vector_store = getVectorStore(embeddings)
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
    
    # Variable which will contain all the splits (chunks)
    all_splits = []

    # Step 5 - Load Each PDF using PyPDF Loader
    for pdfs in pdf_files:
        try: 
            loader = PyPDFLoader(file_path=pdfs)
            raw_docs = loader.load()

            # Step 6 - Chunk and Split Each of the loaded split
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=3000,           # ~750 words, ~512 tokens
                chunk_overlap=300,         # 10% overlap
                length_function=len,       # Measures by characters
                separators=[
                    "\n## ",               # Major sections (Markdown headers) - SINGLE backslash
                    "\n### ",              # Subsections - SINGLE backslash
                    "\n#### ",             # Sub-subsections - SINGLE backslash
                    "\n\n",                # Paragraph breaks - SINGLE backslash
                    "\n",                  # Line breaks - SINGLE backslash
                    ". ",                  # Sentences
                    " ",                   # Words
                    ""                     # Characters (fallback)
                ],
                keep_separator=True,       # Keeps headers with content
                is_separator_regex=False   # Literal string matching
            )

            chunks = text_splitter.split_documents(raw_docs)

            # Step 7 - Add the source for citation
            for chunk in chunks:
                chunk.metadata["source"] = os.path.basename(pdfs)

            all_splits.extend(chunks)
            logger.info(f" -> Split into {len(chunks)} chunks.")
            
        except Exception as e:
            logger.error(f"Failed to process {pdfs}: {e}")

    # Step 8 - Upload to Azure
    if all_splits:
        logger.info(f"Uploading {len(all_splits)} chunks to Azure AI Search Index '{settings.AZURE_SEARCH_INDEX_NAME}'...")
        try:
            # Azure Search accepts batches automatically via this method
            vector_store.add_documents(documents=all_splits)
            logger.info("Indexing Complete! The Knowledge Base is ready.")
            logger.info(f"Total chunks indexed: {len(all_splits)}")
        except Exception as e:
            logger.error(f"Failed to upload documents to Azure Search: {e}")
            logger.error("Please check your Azure Search configuration and try again.")
    else:
        logger.warning("No documents were processed.")

if __name__ == "__main__":
    index_docs()


            


