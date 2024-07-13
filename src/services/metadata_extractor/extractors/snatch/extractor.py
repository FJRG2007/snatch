import os, fitz, exifread
from src.utils.basics import terminal

# Types.
from .types.image import extract_image_metadata
from .types.pdf import extract_pdf_metadata

def snatch(filename):
    filename = filename.lower()
    file_format = filename.split(".")[-1]
    file_path = os.path.join("customs/extract_metadata", filename)
    if file_format == "pdf":
        try:
            result = extract_pdf_metadata(file_path)
            terminal("info", f"Extracted tables from PDF: {filename}")
        except Exception as e:
            terminal("error", f"Error extracting tables from PDF {filename}: {e}")
            return "snatch_exception"  # Return empty string if error occurs.
    elif file_format in ["webp", "jpg", "jpeg", "png", "gif", "svg"]:
        try:
            result = extract_image_metadata(file_path)
            terminal("info", f"Extracted info from image: {filename}")
        except Exception as e:
            terminal("error", f"Error extracting tables from image {filename}: {e}")
            return "snatch_exception"  # Return empty string if error occurs.
    else: ...
    print(result)  # Print metadata to terminal.
    return result  # Return metadata as a string.