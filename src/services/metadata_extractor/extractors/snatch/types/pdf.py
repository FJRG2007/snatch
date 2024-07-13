import fitz

def extract_pdf_metadata(file_path):
    doc = fitz.open(file_path)
    tables_text = []
    for page_num in range(len(doc)):
        tables_text.append(f"Page {page_num+1} text: {doc.load_page(page_num).get_text("text")}")
    return "\n\n".join(tables_text)  # Return concatenated text.