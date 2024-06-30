import re
import click
from pytube import YouTube
from rich import print as rprint
from ..utils.downloader import downloader

def typeLink(url):
    # Regular expression patterns for video and playlist URLs.
    video_pattern = r'^https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11}).*$'
    playlist_pattern = r'^https?://(?:www\.)?youtube\.com/(?:watch\?v=\w+&list=|playlist\?list=)([a-zA-Z0-9_-]{10,}).*$'
    
    # Verify if the link matches the video pattern.
    video_match = re.match(video_pattern, url)
    if video_match:
        video_id = video_match.group(1)
        return {"type": "video", "id": video_id}
    
    # Check if the link matches the playlist pattern.
    playlist_match = re.match(playlist_pattern, url)
    if playlist_match:
        playlist_id = playlist_match.group(1)
        return {"type": "playlist", "id": playlist_id}
    
    # If the link does not match any pattern, return None.
    return {"type": "web" }

def youtube(url, dtype, format):
    type = typeLink(url)
    if (dtype == "source"):
        downloader(url)
    elif (dtype == "video"):
        if (type["type"] == "video"):
            if (format in ["mp4", "mp3"] or format == "auto"): 
                YouTube(url).streams.filter(progressive=True, file_extension="mp4" if format == "auto" else format).first().download()
            else: rprint("Error: Invalid download format -> [mp4, mp3].")