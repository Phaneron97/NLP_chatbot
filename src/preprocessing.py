import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            text += page.extract_text()
    return text

def preprocess_pdf_text(text):
    """
    Preprocesses the extracted text by dividing it into sections based on uppercase section headers.
    """
    sections = {}
    current_section = None
    for line in text.split('\n'):
        line = line.strip()
        if line.isupper():  # Assuming section headers are in uppercase
            current_section = line
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
    return {section: " ".join(content) for section, content in sections.items()}
