import unittest
from unittest.mock import patch, MagicMock
from embedding import Embedding

class TestEmbedding(unittest.TestCase):

    @patch('embedding.SentenceTransformer')
    def test_init(self, mock_sentence_transformer):
        model_name = 'all-MiniLM-L6-v2'
        embedding = Embedding(model_name)
        
        mock_sentence_transformer.assert_called_with(model_name)
        self.assertIsInstance(embedding.model, MagicMock)

    @patch('embedding.SentenceTransformer.encode')
    def test_embed_text(self, mock_encode):
        mock_encode.return_value = [[0.1, 0.2, 0.3]]
        embedding = Embedding()
        
        texts = ["test text"]
        result = embedding.embed_text(texts)
        
        mock_encode.assert_called_with(texts)
        self.assertEqual(result, [[0.1, 0.2, 0.3]])

if __name__ == "__main__":
    unittest.main()
