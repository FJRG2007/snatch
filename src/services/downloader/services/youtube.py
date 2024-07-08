import re
import os
from ..downloader import downloader
from pytube import YouTube, Playlist
from ....utils.basics import terminal
from ..converters import convert_mp4_to_audio

def sanitize_url(url): return re.sub(r'android-app://com.google.android.youtube/http/|ios-app://544007664/vnd.youtube/', 'https://', url)  # Remove mobile app prefixes and convert to standard URL format.

def typeLink(url):
    # Sanitize the URL first.
    url = sanitize_url(url)
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
    if playlist_match: return {"type": "playlist", "id": playlist_match.group(1)}
    
    # If the link does not match any pattern, return None.
    return {"type": "web" }

def youtube(url, dtype, format):
    url = sanitize_url(url)
    type = typeLink(url)
    if (dtype == "source"):
        downloader(url)
    elif (dtype == "video"):
        if (type["type"] == "video"):
            if (format in ["mp4", "mp3", "wav"] or format == "auto"):
                try:
                    stream = YouTube(url).streams.filter(progressive=True, file_extension="mp4").first()
                    if (format in ["mp3", "wav"]): convert_mp4_to_audio(os.path.basename(stream.download(output_path="./output/temporal")), format, True, url)
                    print(f"Downloading: {stream.title}")
                except KeyError as e: terminal("e", f"There was an error downloading the video: {e}")
            else: terminal("e", "Invalid download format -> (mp4, mp3).")
        elif (type["type"] == "playlist"):
            if (format in ["mp4", "mp3"] or format == "auto"):
                try:
                    p = Playlist(url)
                    for v in p.videos:
                        print(f"Downloading: {v.title}")
                        if (format == "mp3"): v.streams.filter(progressive=True, only_audio=True).first().download()
                        else: v.streams.filter(progressive=True, file_extension="mp4" if format == "auto" else format).first().download()
                except KeyError as e: terminal("e", f"There was an error downloading the playlist: {e}")
            else: terminal("e", "Invalid download format -> (mp4, mp3).")
        else: terminal("e", "Invalid format.")