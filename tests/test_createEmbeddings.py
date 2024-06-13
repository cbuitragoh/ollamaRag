from src.helpers import create_embeddings, load_docs, add_embeddings_to_pinecone
import unittest
import os
from dotenv import load_dotenv
load_dotenv()

docs = load_docs(os.getenv("DOCS_FOR_EMB_PATH"))

class TestCreateEmbeddings(unittest.TestCase):
    def test_create_embeddings(self):
        result = create_embeddings(docs=docs)	
        if result is None:
            self.fail("not any embeddings")
        elif type(result) is not list:
            self.fail(f"the embeddings must be list type but get {type(result)} type")
        

class TestAddEmbeddingsToPinecone(unittest.TestCase):
    def test_add_embeddings_to_pinecone(self):
        result = create_embeddings(docs=docs)
        add_embeddings_to_pinecone(result)
        if result is None:
            self.fail("not any embeddings")
        elif type(result) is not list:
            self.fail(f"the embeddings must be list type but get {type(result)} type")


if __name__ == '__main__':
    unittest.main()