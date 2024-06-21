import unittest
import os
import shutil
import streamlit as st
from app import (
    scan_data_directory, select_language, select_part, select_year,
    select_file, process_file, handle_user_input
)
from chatbot import Chatbot
from unittest.mock import patch, mock_open

class TestAppFunctions(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_data")
        os.makedirs(self.test_dir, exist_ok=True)

        # Create a dummy directory structure
        self.root_dir = os.path.join(self.test_dir, "root")
        os.makedirs(os.path.join(self.root_dir, "subdir"), exist_ok=True)
        with open(os.path.join(self.root_dir, "file1.pdf"), 'w') as f:
            f.write("Sample text for file1.pdf")
        with open(os.path.join(self.root_dir, "file2.pdf"), 'w') as f:
            f.write("Sample text for file2.pdf")
        with open(os.path.join(os.path.join(self.root_dir, "subdir"), "file3.pdf"), 'w') as f:
            f.write("Sample text for file3.pdf")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scan_data_directory(self):
        structure = scan_data_directory(self.test_dir)
        expected_structure = {
            'root': {
                '_files': ['file1.pdf', 'file2.pdf'],
                'subdir': {
                    '_files': ['file3.pdf']
                }
            }
        }
        self.assertEqual(structure, expected_structure)

    @patch('streamlit.selectbox')
    def test_select_language(self, mock_selectbox):
        mock_selectbox.return_value = "root"
        structure = {
            'root': {
                '_files': ['file1.pdf', 'file2.pdf'],
                'subdir': {
                    '_files': ['file3.pdf']
                }
            }
        }
        result = select_language(structure)
        self.assertEqual(result, "root")

    @patch('streamlit.selectbox')
    def test_select_part(self, mock_selectbox):
        mock_selectbox.return_value = "subdir"
        structure = {
            'root': {
                '_files': ['file1.pdf', 'file2.pdf'],
                'subdir': {
                    '_files': ['file3.pdf']
                }
            }
        }
        result = select_part(structure, "root")
        self.assertEqual(result, "subdir")

    @patch('streamlit.selectbox')
    def test_select_year(self, mock_selectbox):
        mock_selectbox.return_value = "subdir"
        structure = {
            'root': {
                '_files': ['file1.pdf', 'file2.pdf'],
                'subdir': {
                    '_files': ['file3.pdf']
                }
            }
        }
        result = select_year(structure, "root", "subdir")
        self.assertEqual(result, "subdir")

    @patch('streamlit.selectbox')
    def test_select_file(self):
        # Sample directory structure
        structure = {
            "root": {
                "subdir": {
                    "subdir": {
                        "_files": ["file1.pdf", "file2.pdf", "file3.pdf"]
                    }
                }
            }
        }
        print("Structure passed to select_file:", structure)  # Debugging print

        with patch('builtins.open', mock_open(read_data="file content")):
            result = select_file(structure, "root", "subdir", "subdir")
            self.assertEqual(result, "file1.pdf")


    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('streamlit.write')
    @patch('streamlit.error')
    def test_handle_user_input(self, mock_error, mock_write, mock_button, mock_text_input):
        mock_button.return_value = True
        mock_text_input.return_value = "Hello, chatbot"
        
        chatbot = Chatbot()
        st.session_state['responses'] = []
        
        handle_user_input(chatbot)
        
        self.assertIn(('Hello, chatbot', "I'm sorry, I couldn't find any relevant information.", "No source available."), st.session_state['responses'])

    @patch('streamlit.info')
    @patch('streamlit.success')
    @patch('app.extract_text_from_pdf')
    @patch('app.preprocess_pdf_text')
    def test_process_file(self):
        # Setup necessary mocks and data
        language = "root"
        part = "subdir"
        year = "subdir"
        selected_file = "file3.pdf"
        embedded_vector = np.random.rand(300)  # Example embedding
        chatbot.vectordb.add(embedded_vector, ("Sample text for file3.pdf", "Section 1", os.path.join(data_dir, language, part, year, selected_file)))

        print("Vectordb data:", chatbot.vectordb.data.items())  # Debugging print

        with patch('app.embed_text', return_value=embedded_vector):
            with patch('app.extract_text_from_pdf', return_value="Sample text for file3.pdf"):
                result = process_file(language, part, year, selected_file)

        self.assertIn((embedded_vector, "Section 1", os.path.join(data_dir, language, part, year, selected_file)), chatbot.vectordb.data.items())


if __name__ == '__main__':
    unittest.main()
