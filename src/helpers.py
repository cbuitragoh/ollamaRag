# import libraries
import os
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
from src.prompt_templates import basic_template, formal_template


# SETTINGS
KEY = os.environ["OPENAI_API_KEY"]

# function to load the documents for RAG
def load_docs(path:str):
    """
    args:
        path: path to the document
    
    returns:
        documents: list of documents
    """
    from langchain_community.document_loaders import UnstructuredPDFLoader

    try:
        if not os.path.exists(path):
            raise FileNotFoundError
        if not path.endswith((".pdf", ".doc", ".docx")):
            raise ValueError("File must be a PDF o Word document")
        loader = UnstructuredPDFLoader(path)
        return loader.load()
    except Exception as e:
        print("Exception loading documents for RAG: ", e)
        return None
    
    
#function to create pinecone vector dataabase for RAG
def create_pinecone_index(
        index_name:str,
        pinecone_key:str
):
    """
    args:
        index_name: name of the index to create
        pinecone_key: your pinecone key

    returns:
        index: the pinecone index object
    """
    import time
    from pinecone import Pinecone, ServerlessSpec
    pc = Pinecone(api_key=pinecone_key)
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=768, # Replace with your model dimensions
            metric="cosine", # Replace with your model metric
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ) 
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    index = pc.Index(index_name)
    
    return index


#create embeddings from nomic-embed-text model
def create_embeddings(docs):
    """
    args:
        docs: list of documents to embed

    returns:
        embeddings: list of embeddings
    """
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


#add embeddings to pinecone vector database
def create_vectorstore_and_add_embeddings(
        docs,
        index_name:str,
        namespace:str
):
    """
    args:
        docs: list of documents to embed
        index_name: name of the index to create
        namespace: your pinecone namespace

    returns:
        vectorstore: the pinecone vectorstore object
    """
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    # Split and chunk 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_documents(docs)
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        index_name=index_name,
        namespace=namespace,   
    )
    return vectorstore


#add embeddings to pinecone vector database
def add_embeddings_to_pinecone(
        index,
        embeddings,
        namespace:str
):
    """
    args:
        index: the pinecone index object
        embeddings: list of embeddings
        namespace: your pinecone namespace
    
    returns:
        None
    """
    for i, embedding in enumerate(iterable=embeddings, start=1):
        index.upsert(
            vectors=[{"id":str(i), "values": embedding}],
            namespace=namespace
        )


#query the vector database
def query_vector_db(
        vectorstore: PineconeVectorStore,
        query:str
):
    """
    args:
        vectorstore: the pinecone vectorstore object
        query: the query to search for

    returns:
        results: the search results
    """
    try:
        results = vectorstore.similarity_search(query, k=2)
        print(results[0].page_content)
        return results
    except Exception:
        return None
    

# Chat response
def respond_to_message(
        user_input: str = "hello",
        template_name: str = "basic"
):
    """
    args:
        user_input: the user's input message
        template_name: the name of the template to use

    returns:
        response: the bot's response
    """
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