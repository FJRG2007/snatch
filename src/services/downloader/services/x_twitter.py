from tqdm import tqdm
import os, re, bs4, requests
from src.lib.config import config
from urllib.parse import urlparse
from ..downloader import downloader
from src.utils.basics import terminal

def download_video(url, path, file_name) -> None:
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
    download_path = os.path.join(path, file_name)
    with open(download_path, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    terminal("s", "Video downloaded successfully.")

def download_twitter_video(url):
    parsed_url = urlparse(url)
    download_path = f"output/downloads/{parsed_url.netloc}/{parsed_url.path.strip('/').replace('/', '-')}"
    if (True): # Coming Soon.
        try:
            api_url = f"https://twitsave.com/info?url={url}"
            response = requests.get(api_url)
            data = bs4.BeautifulSoup(response.text, "html.parser")
            download_button = data.find_all("div", class_="origin-top-right")[0]
            quality_buttons = download_button.find_all("a")
            highest_quality_url = quality_buttons[0].get("href") # Highest quality video url
            file_name = data.find_all("div", class_="leading-tight")[0].find_all("p", class_="m-2")[0].text # Video file name
            file_name = re.sub(r"[^a-zA-Z0-9]+", " ", file_name).strip() + ".mp4" # Remove special characters from file name
            download_video(highest_quality_url, download_path, file_name)
        except IndexError as e: terminal("e", f"Video not found in the publication.")
    else:
        ...

def download(url, dtype, format):
    if (dtype == "source"): downloader(url)
    elif (dtype == "video"):
        if (format in ["mp4"] or format == "auto"): download_twitter_video(url)
        else: terminal("e", "[Invalid download format -> (mp4).")