import streamlit as st
from chatbot import Chatbot
from preprocessing import extract_text_from_pdf, preprocess_pdf_text

def main():
    st.title("Inholland University Chatbot")
    chatbot = Chatbot()

    if 'responses' not in st.session_state:
        st.session_state['responses'] = []

    pdf_path = 'data/Educationguide compleet 2022-2023 Engels .pdf'
    raw_text = extract_text_from_pdf(pdf_path)
    sections = preprocess_pdf_text(raw_text)

    for section, content in sections.items():
        vector = chatbot.embedding.embed_text([content])[0]
        chatbot.vectordb.add_item(section, vector)

    user_input = st.text_input("You: ", key="input")

    if st.button("Send"):
        response = chatbot.generate_response(user_input)
        st.session_state['responses'].append((user_input, response))

    if st.session_state['responses']:
        for user, bot in st.session_state['responses']:
            st.write(f"You: {user}")
            st.write(f"Bot: {bot}")

if __name__ == "__main__":
    main()
