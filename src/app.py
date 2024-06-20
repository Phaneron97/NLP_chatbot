import streamlit as st
import os
from chatbot import Chatbot
from preprocessing import extract_text_from_pdf, preprocess_pdf_text

def scan_data_directory(root_dir):
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
    return st.selectbox("Select Language", [k for k in structure.keys() if k != '_files'])

def select_part(structure, language):
    return st.selectbox("Select Part", [k for k in structure[language].keys() if k != '_files'])

def select_year(structure, language, part):
    return st.selectbox("Select Year", [k for k in structure[language][part].keys() if k != '_files'])

def select_file(structure, language, part, year):
    files = structure[language][part][year].get('_files', [])
    if files:
        return st.selectbox("Select File", files)
    return None

def process_file(chatbot, data_dir, language, part, year, selected_file):
    pdf_path = os.path.join(data_dir, language, part, year, selected_file)
    print(f"Processing file: {pdf_path}")
    raw_text = extract_text_from_pdf(pdf_path)
    sections = preprocess_pdf_text(raw_text)

    for section, content in sections.items():
        vector = chatbot.embedding.embed_text([content])[0]
        chatbot.vectordb.add_item((content, section, pdf_path), vector)  # Store content with source section and file path

def main():
    st.title("Inholland University Chatbot")
    chatbot = Chatbot()

    if 'responses' not in st.session_state:
        st.session_state['responses'] = []

    data_dir = "data"
    structure = scan_data_directory(data_dir)
    
    language = select_language(structure)
    
    if language:
        part = select_part(structure, language)
        
        if part:
            year = select_year(structure, language, part)
            
            if year:
                selected_file = select_file(structure, language, part, year)
                
                if selected_file:
                    process_file(chatbot, data_dir, language, part, year, selected_file)
                    st.success(f"Processed file: {selected_file}")

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

if __name__ == "__main__":
    main()
