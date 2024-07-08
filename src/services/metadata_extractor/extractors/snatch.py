import os, fitz, exifread
from src.utils.basics import terminal

def extract_image_metadata(file_path):
    with open(file_path, "rb") as f:
        tags = exifread.process_file(f)
        metadata = []
        for tag, value in tags.items():
            metadata.append(f"{tag}: {value}")
        return "\n".join(metadata)  # Return metadata as text.

def extract_pdf_tables(file_path):
    doc = fitz.open(file_path)
    tables_text = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        tables_text.append(f"Page {page_num+1} text: {text}")
    return "\n\n".join(tables_text)  # Return concatenated text.

def snatch(filename):
    file_path = os.path.join("customs/extract_metadata", filename)
    if filename.lower().endswith(".pdf"):
        try:
            result = extract_pdf_tables(file_path)
            terminal("info", f"Extracted tables from PDF: {filename}")
        except Exception as e:
            terminal("error", f"Error extracting tables from PDF {filename}: {e}")
            return "snatch_exception"  # Return empty string if error occurs.
    else: result = extract_image_metadata(file_path)
    print(result)  # Print metadata to terminal.
    return result  # Return metadata as a string.