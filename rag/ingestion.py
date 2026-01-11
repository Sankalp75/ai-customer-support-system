
import os
import logging
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping from file extension to loader class
LOADER_MAPPING = {
    ".pdf": PyPDFLoader,
    ".md": UnstructuredMarkdownLoader,
    ".txt": TextLoader,
}


def load_documents(path: str):
    """
    Load documents from the specified directory path, choosing loader based on file extension.
    """
    logger.info(f"Loading documents from {path}")
    documents = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            ext = "." + file.split(".")[-1]
            if ext in LOADER_MAPPING:
                logger.info(f"Loading {file_path} with {LOADER_MAPPING[ext].__name__}")
                loader_class = LOADER_MAPPING[ext]
                loader = loader_class(file_path)
                documents.extend(loader.load())
            else:
                logger.warning(f"No loader found for file extension {ext}, skipping {file_path}")

    logger.info(f"Loaded {len(documents)} documents.")
    return documents


def split_documents(documents):
    """
    Split documents into smaller chunks.
    """
    logger.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split documents into {len(chunks)} chunks.")
    return chunks


def create_vector_store(chunks):
    """
    Create and persist a FAISS vector store from document chunks.
    """
    logger.info("Creating embeddings and vector store...")
    
    # Initialize the embedding function
    embedding_function = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME
    )
    
    # Create the FAISS vector store
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_function,
    )
    
    # Persist the vector store
    vector_store.save_local(settings.VECTOR_STORE_DIR)
    
    logger.info(f"Vector store created and persisted at {settings.VECTOR_STORE_DIR}")
    return vector_store


def main():
    """
    Main function for the ingestion pipeline.
    """
    documents = load_documents(settings.KNOWLEDGE_BASE_DIR)
    if not documents:
        logger.warning("No documents found to ingest.")
        return
        
    chunks = split_documents(documents)
    create_vector_store(chunks)
    logger.info("Ingestion process completed successfully.")

if __name__ == "__main__":
    main()
