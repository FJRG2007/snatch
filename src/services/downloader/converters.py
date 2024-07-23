import os
from urllib.parse import urlparse
from src.utils.basics import terminal
from moviepy.editor import VideoFileClip

def convert_mp4_to_audio(input_file, output_format, del_original, url):
    try:
        parsed_url = urlparse(url)
        # Get the absolute path of the input file.
        input_path = os.path.abspath(f"./output/temporal/{input_file}")
        # Load the MP4 file using moviepy.
        video = VideoFileClip(input_path)
        # Extract audio from the video.
        audio = video.audio
        # Set the output path.
        output_path = os.path.join(f"output/downloads/{parsed_url.netloc}/{parsed_url.path.strip("/").replace("/", "-")}", f"{os.path.splitext(input_file)[0]}.{output_format}")
        # Write the audio to the output file.
        audio.write_audiofile(output_path)
        video.close()
        if (del_original): os.remove(input_path) # Remove original file.
        terminal("s", f"[green]Successful conversion. File saved as: {output_path}")
    except Exception as e: terminal("e", f"Error during conversion of file '{input_file}' (path: {input_path}): {e}")