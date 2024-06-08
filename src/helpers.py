# import libraries
import os
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from src.prompt_templates import basic_template, formal_template

from .logger import create_logger
from dotenv import load_dotenv
load_dotenv()

# SETTINGS
KEY = os.environ["OPENAI_API_KEY"]

# function to load the documents for RAG
def load_docs(path:str):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError
        if not path.endswith((".pdf", ".doc", ".docx")):
            raise ValueError("File must be a PDF o Word document")
        loader = UnstructuredPDFLoader(path)
        return loader.load()
    except Exception:
        logger.error("Error loading document")
        return None
    

# Chat response
def respond_to_message(
        user_input: str = "hello",
        template_name: str = "basic"
):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=KEY)
    if template_name == "basic":
        base_template = basic_template
        prompt = PromptTemplate.from_template(template=base_template)
    else:
        base_template = formal_template
        prompt = ChatPromptTemplate.from_messages(base_template)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    # Process the incoming message
    response = chain.invoke({"user_input": user_input})
    return response