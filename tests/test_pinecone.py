from dotenv import load_dotenv
load_dotenv()
import os


print("creating index...") 
index_name = os.getenv("PINECONE_INDEX_NAME")
print("index_name: ", index_name)
pinecone_key = os.getenv("PINECONE_API_KEY")
print("pinecone_key: ", pinecone_key)
#create_pinecone_index(index_name, pinecone_key)