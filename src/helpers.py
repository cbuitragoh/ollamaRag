# import libraries
import os
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from src.prompt_templates import basic_template, formal_template

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
        return None
    
#function to create pinecone vector dataabase for RAG
def create_pinecone_index(
        index_name:str,
        pinecone_key:str
):
    try:
        from pinecone import Pinecone, ServerlessSpec
        pc = Pinecone(api_key=pinecone_key)
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1536, # Replace with your model dimensions
                metric="cosine", # Replace with your model metric
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ) 
            )
    except Exception:
        return None

#create embeddings from nomic-embed-text model
def create_embeddings(docs):
    try:
        from langchain_community.embeddings import OllamaEmbeddings
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        # Split and chunk 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)
        ollama_emb = OllamaEmbeddings(
            model="nomic-embed-text"
        )
        embeddings = ollama_emb.embed_documents(chunks)
        return embeddings
    
    except Exception:
        return None

#add embeddings to pinecone vector database
def add_embeddings_to_pinecone(
        embeddings,
        index_name:str,
        namespace:str
):
    try:
        from langchain_pinecone import PineconeVectorStore
        vectorstore = PineconeVectorStore(
            index_name=index_name,
            namespace=namespace,
            embedding=embeddings
        )
        return vectorstore
    except Exception:
        return None    

#query the vector database
def query_vector_db(
        vectorstore,
        query:str
):
    try:
        from langchain_pinecone import PineconeSearch
        search = PineconeSearch.from_vectorstore(vectorstore)
        results = search.similarity_search(query, k=5)
        return results
    except Exception:
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