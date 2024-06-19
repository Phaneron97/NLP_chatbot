import streamlit as st
from chatbot import Chatbot
from preprocessing import extract_text_from_pdf, preprocess_pdf_text, scan_data_directory
import os

def get_cached_data():
    return {}

def get_years(language, doc_type):
    base_path = os.path.join('data', doc_type, language)
    return [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

def get_educations(language, doc_type, year):
    base_path = os.path.join('data', doc_type, language, year)
    return [file for file in os.listdir(base_path) if file.endswith(".pdf")]

def process_pdf(chatbot, pdf_path, update_progress):
    raw_text = extract_text_from_pdf(pdf_path)
    print("Raw text from PDF:", raw_text)  # Debug: Print raw text
    sections = preprocess_pdf_text(raw_text)
    print("Preprocessed sections:", sections)  # Debug: Print sections

    num_sections = len(sections)
    for i, (section, content) in enumerate(sections.items()):
        vector = chatbot.embedding.embed_text([content])[0]
        print(f"Embedding for section {section}:", vector)  # Debug: Print vector
        chatbot.vectordb.add_item((content, section, pdf_path), vector)  # Store content with source section and file path
        update_progress(int((i + 1) / num_sections * 100))

def main():
    st.title("Inholland University Chatbot")
    chatbot = Chatbot()
    cached_data = get_cached_data()

    if 'responses' not in st.session_state:
        st.session_state['responses'] = []

    # Step 1: Select Language
    language = st.radio("Select Language:", ('English', 'Dutch'))

    # Step 2: Select Document Type (OER or Onderwijsgids)
    doc_type = st.radio("Select Document Type:", ('OER', 'Onderwijsgids'))

    # Step 3: Select Year
    years = get_years(language, doc_type)
    year = st.selectbox("Select Year of Study:", years)

    # Step 4: Select Education
    educations = get_educations(language, doc_type, year)
    education = st.selectbox("Select Education Program:", educations)

    submitted = st.button("Submit")

    if submitted:
        # Process the selected PDF only if an education is selected
        if education:
            pdf_path = os.path.join('data', doc_type, language, year, education)
            if pdf_path not in cached_data:
                progress = st.progress(0)
                progress_text = st.empty()

                def update_progress(percent):
                    progress.progress(percent)
                    progress_text.text(f"Processing: {percent}%")

                # Process PDF on the main thread
                process_pdf(chatbot, pdf_path, update_progress)

                st.success("Processing completed")
                cached_data[pdf_path] = chatbot.vectordb

            st.session_state['pdf_path'] = pdf_path

    if 'pdf_path' in st.session_state:
        user_input = st.text_input("You: ", key="input")

        if st.button("Send"):
            response, source = chatbot.generate_response(user_input)
            st.session_state['responses'].append((user_input, response, source))

    if st.session_state['responses']:
        for user, bot, source in st.session_state['responses']:
            st.write(f"You: {user}")
            st.write(f"Bot: {bot}")
            st.write(f"Source: {source}")

if __name__ == "__main__":
    main()
