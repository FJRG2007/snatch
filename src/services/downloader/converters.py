import os
from rich import print as rprint
from moviepy.editor import VideoFileClip
from urllib.parse import urljoin, urlparse

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
        output_path = os.path.join(f"output/downloads/{parsed_url.netloc}/{parsed_url.path.strip('/').replace('/', '-')}", os.path.splitext(input_file)[0] + f".{output_format}")
        # Write the audio to the output file.
        audio.write_audiofile(output_path)
        video.close()
        if (del_original): os.remove(input_path) # Elminates the original file.
        rprint(f"[green]Successful conversion. File saved as: {output_path}[/green]")
    except Exception as e: rprint(f"[red]Error during conversion of file '{input_file}' (path: {input_path}): {e}[/red]")