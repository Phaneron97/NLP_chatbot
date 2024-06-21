import unittest
from unittest.mock import patch, mock_open, MagicMock
import PyPDF2
from preprocessing import extract_text_from_pdf, preprocess_pdf_text

class TestPreprocessing(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="Dummy PDF content")
    @patch('PyPDF2.PdfReader')
    def test_extract_text_from_pdf(self, mock_pdf_reader, mock_open_file):
        # Simulate PDF Reader pages with mocked extract_text method
        mock_pdf_reader.return_value.pages = [MagicMock(extract_text=lambda: "Page 1 text"), MagicMock(extract_text=lambda: "Page 2 text")]

        # Dummy path for testing
        pdf_path = "C:/Users/ninow/Documents/GitHub/NLP_chatbot/data"
        result = extract_text_from_pdf(pdf_path)
        
        self.assertEqual(result, "Page 1 textPage 2 text")

    def test_preprocess_pdf_text(self):
        text = "SECTION 1\nThis is some text.\nSECTION 2\nThis is some more text."
        expected_result = {
            "SECTION 1": "This is some text.",
            "SECTION 2": "This is some more text."
        }
        
        result = preprocess_pdf_text(text)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
