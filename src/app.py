import streamlit as st
from chatbot import Chatbot
from preprocessing import extract_text_from_pdf, preprocess_pdf_text, scan_data_directory

def main():
    st.title("Inholland University Chatbot")
    chatbot = Chatbot()

    if 'responses' not in st.session_state:
        st.session_state['responses'] = []

    data_dir = 'data'  # Base data directory
    pdf_files = scan_data_directory(data_dir)
    
    for pdf_path in pdf_files:
        raw_text = extract_text_from_pdf(pdf_path)
        sections = preprocess_pdf_text(raw_text)

        for section, content in sections.items():
            vector = chatbot.embedding.embed_text([content])[0]
            chatbot.vectordb.add_item((content, section, pdf_path), vector)  # Store content with source section and file path

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
