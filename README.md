# NLP Chatbot

group: <group number>
delivery date: %Y%m%dT%H%M%SZ
Members:
- Student 1 (123456)
- Student 2 (246824)
- Student 3 (321123)
- <student name> (<student number>)

## Introduction
This project involves creating a chatbot using Streamlit and Ollama that can answer questions about the OER data.

## Code structure
- `preprocessing.py`: Contains code for preprocessing OER files.
- `embedding.py`: Contains the Embedding class for converting text to vectors.
- `vectordb.py`: Contains the VectorDB class for storing and querying vectors.
- `chatbot.py`: Contains the Chatbot class for generating responses.
- `app.py`: Contains the Streamlit app interface.

## How to Run
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
