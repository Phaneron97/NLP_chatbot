import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text()
    return text

def preprocess_pdf_text(text):
    sections = {}
    current_section = None
    paragraph = ""
    page = None
    
    for line in text.split('\n'):
        print(line)
        line = line.strip()
        if line.startswith('--- Page'):
            page = line
        elif line.isupper():  # Assuming section headers are in uppercase
            if current_section and paragraph:
                sections[current_section] += f" {paragraph} (Source: {page})"
                paragraph = ""
            current_section = line
            if current_section not in sections:
                sections[current_section] = f"(Source: {page})"
        elif current_section:
            if line == "":
                if paragraph:
                    sections[current_section] += f" {paragraph} (Source: {page})"
                    paragraph = ""
            else:
                if paragraph:
                    paragraph += f" {line}"
                else:
                    paragraph = line
    
    # Add any remaining paragraph to the last section
    if current_section and paragraph:
        sections[current_section] += f" {paragraph} (Source: {page})"
        print(sections)
    return sections

def scan_data_directory(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    print(pdf_files)
    return pdf_files
