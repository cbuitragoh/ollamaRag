import unittest
import os
from dotenv import load_dotenv
load_dotenv()

from src.helpers import respond_to_message, load_docs
from src.app import create_logger

class TestHelpers(unittest.TestCase):
    def test_respond_to_message(self):
        self.assertEqual(respond_to_message("Hello"), "Hello")

class TestLogger(unittest.TestCase):
    def test_create_logger(self):
        logger = create_logger("my_logger")
        logger.info("Test message")

class TestLoaderDocs(unittest.TestCase):
    def test_load_docs(self):
        load_docs(os.getenv("LOCAL_PATH"))
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()