import streamlit as st
import os
from chatbot import Chatbot
from preprocessing import extract_text_from_pdf, preprocess_pdf_text

def scan_data_directory(root_dir):
    """
    Scans the given root directory and constructs a nested dictionary representing the file structure.
    """
    structure = {}
    for root, dirs, files in os.walk(root_dir):
        relative_path = os.path.relpath(root, root_dir)
        parts = relative_path.split(os.sep)
        current_level = structure
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        current_level['_files'] = files
    return structure

def select_language(structure):
    """
    Displays a dropdown for selecting the language.
    """
    return st.selectbox("Select Language", ["please select your language"] + [k for k in structure.keys() if k != '_files'])

def select_part(structure, language):
    """
    Displays a dropdown for selecting the part.
    """
    return st.selectbox("Select Part", ["please select your part"] + [k for k in structure[language].keys() if k != '_files'])

def select_year(structure, language, part):
    """
    Displays a dropdown for selecting the year.
    """
    return st.selectbox("Select Year", ["please select your year"] + [k for k in structure[language][part].keys() if k != '_files'])

def select_file(structure, language, part, year):
    """
    Displays a dropdown for selecting the file.
    """
    files = structure[language][part][year].get('_files', [])
    if files:
        return st.selectbox("Select File", ["please select your file"] + files)
    return None

def process_file(chatbot, data_dir, language, part, year, selected_file):
    """
    Processes the selected file and updates the chatbot's vector database with the extracted text sections.
    """
    pdf_path = os.path.join(data_dir, language, part, year, selected_file)
    st.info(f"Processing file: {pdf_path}")
    raw_text = extract_text_from_pdf(pdf_path)
    sections = preprocess_pdf_text(raw_text)

    for section, content in sections.items():
        vector = chatbot.embedding.embed_text([content])[0]
        chatbot.vectordb.add_item((content, section, pdf_path), vector)  # Store content with source section and file path

def handle_user_input(chatbot):
    """
    Handles user input and displays the chat responses.
    """
    user_input = st.text_input("You: ", key="input")

    if st.button("Send") and user_input:
        if chatbot:
            response, source = chatbot.generate_response(user_input)
            st.session_state['responses'].append((user_input, response, source))
        else:
            st.error("No data available in the vector database. Please select and process a file first.")

    if st.session_state['responses']:
        for user, bot, source in st.session_state['responses']:
            st.write(f"You: {user}")
            st.write(f"Bot: {bot}")
            st.write(f"Source: {source}")

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Inholland University Chatbot")
    chatbot = Chatbot()

    if 'responses' not in st.session_state:
        st.session_state['responses'] = []

    data_dir = "data"
    structure = scan_data_directory(data_dir)
    
    # Select language
    language = select_language(structure)
    
    if language and language != "please select your language":
        # Select part
        part = select_part(structure, language)
        
        if part and part != "please select your part":
            # Select year
            year = select_year(structure, language, part)
            
            if year and year != "please select your year":
                # Select file
                selected_file = select_file(structure, language, part, year)
                
                if selected_file and selected_file != "please select your file":
                    # Process selected file
                    process_file(chatbot, data_dir, language, part, year, selected_file)
                    st.success(f"Processed file: {selected_file}")
                    
                    # Handle user input and chat responses
                    handle_user_input(chatbot)

if __name__ == "__main__":
    main()
