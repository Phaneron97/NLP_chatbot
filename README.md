# NLP Chatbot

group: De Kaaseters
delivery date: 21-06-2024
Members:
- Christian Wanschers (632748)
- Bastiaan Verheul (667382)
- Nino van Alphen (675273)

## Introduction
This project involves creating a chatbot using Streamlit and Ollama that can answer questions about the OER data. 
The chatbot makes use of `all-MiniLM-L6-v2` using the `SentenceTransformer` library.
The user may pick a PDF by navigating the included dropdowns in the form at the start of each conversation.

The form includes selection the language (English or Dutch), the documenttype (OER or onderwijsgids), the releaseyear of the document, 
and the specific PDF file present in the built navigation path based on the form.
After submitting which PDF the user wants to check out the chosen PDF is extracted, preprocessed and stored as a vector using vectorDB for querying.

The Chatbot class handles the text extraction of the PDF by organising it into sections based on uppercase headers.
After the user inputs a search query, the query is converted to a vector using the embedding model. The vectorquery is then used to search the vectorDB for the most similar content and responds with the most relevant text section.
The textsection is limited to 1000 character or by finding the end of the sentence once this limit has been reached.

The project runs locally using streamlit which handles the frontend on your default webbrowser.

## Code structure
- `preprocessing.py`: Contains code for preprocessing OER files.
   -  `extract_text_from_pdf()`: Extracts text frp, a PDF file.
   -  `preprocess_pdf_text()`: Preprocesses the extracted text by dividing it into sections based on uppercase section headers.
- `embedding.py`: Contains the Embedding class for converting text to vectors.
   - `__init__()`: Loads the model `all-MiniLM-L6-v2`
   - `embed_text()`: Generates embeddings for a list of texts.
- `vectordb.py`: Contains the VectorDB class for storing and querying vectors.
   - `__init__()`: Loads an empty vectorDB instance.
   - `add_item()`: Adds an item (in this case the content related to the section and the section itself) and the corresponding vector.
   - `search()`: Searches for the most similar item in the database to the query vector.
- `chatbot.py`: Contains the Chatbot class for generating responses.
   - `__init__()`: Loads a chatbot with a model and a vectorDB.
   - `generate_response()`: Generates the response based on the vector similarity.
   - `truncate_response()`: Truncates the chatbots output to a maximum length (in this case 1000 character) without cutting off the last sentence.
- `app.py`: Contains the Streamlit app interface.
   - `scan_data_directory()`: Scans the given root directory and constructs a nested dictionary representing the file structure.
   - `select_language()`: Displays a dropdown for selecting the language.
   - `select_part()`: Displays a dropdown for selecting the part.
   - `select_year()`: Displays a dropdown for selecting the year.
   - `select_file()`: Displays a dropdown for selecting the file.
   - `process_file()`: Processes the selected file and updates the chatbot's vector database with the extracted text sections.
   - `handle_user_input()`: Handles user input and displays the chat responses.
   - `main()`: Main function of the app.

## How to Run
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate # Windows: .venv\Scripts\activate
   pip install -r requirements.txt

2. Run the application
   ```bash
   streamlit run src/app.py
