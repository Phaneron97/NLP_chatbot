import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            text += page.extract_text()
    return text

def preprocess_pdf_text(text, chunk_size=10):
    sections = {}
    current_section = None
    lines = text.split('\n')
    chunk = []
    
    for line in lines:
        line = line.strip()
        if line.isupper():  # Assuming section headers are in uppercase
            if current_section and chunk:
                sections[current_section].append(" ".join(chunk))
                chunk = []
            current_section = line
            if current_section not in sections:
                sections[current_section] = []
        elif current_section:
            chunk.append(line)
            if len(chunk) >= chunk_size:
                sections[current_section].append(" ".join(chunk))
                chunk = []
    
    # Add any remaining chunk to the last section
    if current_section and chunk:
        sections[current_section].append(" ".join(chunk))
    
    return sections
