from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
import os
from .logger import create_logger
from dotenv import load_dotenv
load_dotenv()


def load_docs(path:str):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError
        if not path.endswith((".pdf", ".doc", ".docx")):
            raise ValueError("File must be a PDF o Word document")
        loader = UnstructuredPDFLoader(path)
        return loader.load()
    except Exception:
        logger = create_logger()
        logger.error("Error loading document")
        return None
