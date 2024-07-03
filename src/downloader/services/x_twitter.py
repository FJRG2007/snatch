
import os
import re
import bs4
import requests
from tqdm import tqdm
from rich import print as rprint
from src.lib.config import config
from ..downloader import downloader
from urllib.parse import urljoin, urlparse

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
    print("Video downloaded successfully!")


def download_twitter_video(url):
    parsed_url = urlparse(url)
    download_path = f"downloads/{parsed_url.netloc}/{parsed_url.path.strip("/").replace("/", "-")}"
    if (config.platforms.x_twitter.useNoAuthResource):
        try:
            api_url = f"https://twitsave.com/info?url={url}"

            response = requests.get(api_url)
            data = bs4.BeautifulSoup(response.text, "html.parser")
            download_button = data.find_all("div", class_="origin-top-right")[0]
            quality_buttons = download_button.find_all("a")
            highest_quality_url = quality_buttons[0].get("href") # Highest quality video url
    
            file_name = data.find_all("div", class_="leading-tight")[0].find_all("p", class_="m-2")[0].text # Video file name
            file_name = re.sub(r"[^a-zA-Z0-9]+", ' ', file_name).strip() + ".mp4" # Remove special characters from file name
    
            download_video(highest_quality_url, download_path, file_name)
        except IndexError as e:
            rprint(f"[red]Error: Video not found in the publication.[/red]")
    else:
        pass

def x_twitter(url, dtype, format):
    if (dtype == "source"):
        downloader(url)
    elif (dtype == "video"):
        if (format in ["mp4"] or format == "auto"):
            download_twitter_video(url)
        else: rprint("[red]Error: Invalid download format -> (mp4).[/red]")