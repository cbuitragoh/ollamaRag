import unittest

from src.helpers import respond_to_message
from src.app import create_logger

class TestHelpers(unittest.TestCase):
    def test_respond_to_message(self):
        self.assertEqual(respond_to_message("Hello"), "Hello")

class TestLogger(unittest.TestCase):
    def test_create_logger(self):
        logger = create_logger("my_logger")
        logger.info("Test message")



if __name__ == '__main__':
    unittest.main()