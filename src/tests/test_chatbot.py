import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from chatbot import Chatbot

class TestChatbot(unittest.TestCase):

    def setUp(self):
        self.chatbot = Chatbot()

    @patch('embedding.Embedding.embed_text')
    @patch('vectordb.VectorDB.search')
    def test_generate_response_found(self, mock_search, mock_embed_text):
        mock_embed_text.return_value = [np.array([1, 2, 3])]
        mock_search.return_value = ("Best match text.", "Section 1", "file1.pdf")
        
        response, source = self.chatbot.generate_response("test input")
        
        self.assertEqual(response, "Best match text.")
        self.assertEqual(source, "Section 1, from file: file1.pdf")

    @patch('embedding.Embedding.embed_text')
    @patch('vectordb.VectorDB.search')
    def test_generate_response_not_found(self, mock_search, mock_embed_text):
        mock_embed_text.return_value = [np.array([1, 2, 3])]
        mock_search.return_value = None
        
        response, source = self.chatbot.generate_response("test input")
        
        self.assertEqual(response, "I'm sorry, I couldn't find any relevant information.")
        self.assertEqual(source, "No source available.")

    def test_truncate_response(self):
        long_text = "This is a very long text. " * 50
        expected_truncated = long_text[:1000]
        
        truncated_text = self.chatbot.truncate_response(long_text, 1000)
        
        self.assertTrue(truncated_text.endswith('.'))
        self.assertLessEqual(len(truncated_text), 1000)

    def test_truncate_response_no_period(self):
        long_text = "ThisIsAVeryLongTextWithoutAnyPeriod " * 50
        expected_truncated = long_text[:1000] + "..."
        
        truncated_text = self.chatbot.truncate_response(long_text, 1000)
        
        self.assertEqual(truncated_text, expected_truncated)

if __name__ == "__main__":
    unittest.main()
