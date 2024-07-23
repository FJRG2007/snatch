from tqdm import tqdm
import os, re, bs4, requests
from urllib.parse import urlparse
from ..downloader import downloader
from src.utils.basics import terminal

def download_video(url, path, file_name) -> None:
    response = requests.get(url, stream=True)
    progress_bar = tqdm(total=int(response.headers.get("content-length", 0)), unit="B", unit_scale=True)
    with open(os.path.join(path, file_name), "wb") as file:
        for data in response.iter_content(1024):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    terminal("s", "Video downloaded successfully.")

def download_twitter_video(url):
    parsed_url = urlparse(url)
    download_path = f"output/downloads/{parsed_url.netloc}/{parsed_url.path.strip('/').replace('/', '-')}"
    if (True): # Coming Soon.
        try:
            response = requests.get(f"https://twitsave.com/info?url={url}")
            data = bs4.BeautifulSoup(response.text, "html.parser")
            download_video(data.find_all("div", class_="origin-top-right")[0].find_all("a")[0].get("href"), download_path, re.sub(r"[^a-zA-Z0-9]+", " ", data.find_all("div", class_="leading-tight")[0].find_all("p", class_="m-2")[0].text).strip() + ".mp4")
        except IndexError as e: terminal("e", f"Video not found in the publication.")
    else:
        ... # Coming Soon.

def download(url, dtype, format):
    if (dtype == "source"): downloader(url)
    elif (dtype == "video"):
        if (format in ["mp4"] or format == "auto"): download_twitter_video(url)
        else: terminal("e", "[Invalid download format -> (mp4).")