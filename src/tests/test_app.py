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
import numpy as np

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

    # def test_scan_data_directory(self):
    #     expected_structure = {
    #         'root': {
    #             '_files': ['file1.pdf', 'file2.pdf'],
    #             'subdir': {
    #                 '_files': ['file3.pdf']
    #             }
    #         }
    #     }
    #     structure = scan_data_directory(self.root_dir)
    #     self.assertEqual(structure, expected_structure)

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
    def test_select_file(self, mock_selectbox):
        mock_selectbox.return_value = "file1.pdf"
        structure = {
            "root": {
                "subdir": {
                    "subdir": {
                        "_files": ["file1.pdf", "file2.pdf", "file3.pdf"]
                    }
                }
            }
        }
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

    # @patch('app.process_file')
    # def test_process_file(self, mock_process_file):
    #     language = "root"
    #     part = "subdir"
    #     year = "subdir"
    #     selected_file = "file3.pdf"
    #     embedded_vector = np.random.rand(300)  # Example embedding

    #     chatbot = Chatbot()  # Assuming `Chatbot` initializes `VectorDB`
    #     chatbot.vectordb = {}  # Replace this with your actual initialization
        
    #     # Replace `VectorDB.add` with your actual method to add vectors
    #     chatbot.vectordb.add = lambda vector, metadata: None  # Replace with actual implementation

    #     with patch('app.embed_text', return_value=embedded_vector):
    #         with patch('app.extract_text_from_pdf', return_value="Sample text for file3.pdf"):
    #             result = process_file(language, part, year, selected_file)

    #     # Add assertions related to `VectorDB` operations here
    #     # Example:
    #     # self.assertIn((embedded_vector, "Section 1", os.path.join(self.root_dir, language, part, year, selected_file)), chatbot.vectordb.data.items())

    #     # Mock `process_file` return value example:
    #     mock_process_file.return_value = "Expected result"
    #     result = process_file("file_path")
    #     self.assertEqual(result, "Expected result")


if __name__ == '__main__':
    unittest.main()
