import os
import ffmpeg # pip install ffmpeg-python
from rich import print as rprint

def convert_mp4_to_audio(input_file, output_format):
    try:
        input_path = os.path.abspath(f"./temporal/{input_file}")
        print(input_path)
        
        # Upload MP4 file.
        stream = ffmpeg.input(input_path)
        
        # Extract audio from MP4 file.
        audio = stream.audio
        
        # Set the output format.
        output_path = os.path.join("./temporal")
        if output_format == "mp3": 
            audio = ffmpeg.output(audio, output_path, f=output_format, ab="192k")
        elif output_format == "wav":
            audio = ffmpeg.output(audio, output_path, f=output_format)
        else:
            return rprint("[red]Invalid output format. Choose mp3 or wav.[/red]")
        
        ffmpeg.run(audio)
        rprint(f"[green]Successful conversion. File saved as: {output_path}[/green]")
    
    except Exception as e:
        rprint(f"[red]Error during conversion: {e}[/red]")