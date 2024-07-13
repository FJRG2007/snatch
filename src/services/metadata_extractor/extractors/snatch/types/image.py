import exifread

def extract_image_metadata(file_path):
    with open(file_path, "rb") as f:
        metadata = []
        for tag, value in exifread.process_file(f).items():
            metadata.append(f"{tag}: {value}")
        return "\n".join(metadata)  # Return metadata as text.