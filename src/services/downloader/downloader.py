import os, requests
import src.lib.colors as cl
from bs4 import BeautifulSoup
from datetime import datetime
from src.utils.basics import terminal
from urllib.parse import urljoin, urlparse

def download_resource(url, destination_folder):
    if not url.startswith("http"): return
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Extract the filename from the URL.
            filename = os.path.basename(urlparse(url).path)
            # Save the resource in the destination folder.
            with open(os.path.join(destination_folder, filename), "wb") as file:
                file.write(response.content)
        else: terminal("e", f"Failed to download the resource. Status code: {response.status_code}")
    except Exception as e: terminal("e", f"Error downloading the resource {url}: {str(e)}.")

def downloader(url):
    print("-" * 50)
    print(f"Scanning url: {url}")
    print(f"Scanning started at: {str(datetime.now())}")
    print("-" * 50) 
    parsed_url = urlparse(url)
    destination_folder = f"output/downloads/{parsed_url.netloc}/{parsed_url.path.strip('/').replace('/', '-')}"
    # Get the content of the URL.
    response = requests.get(url)
    if response.status_code == 200:
        # Create the destination folder if it doesn"t exist.
        if not os.path.exists(destination_folder): os.makedirs(destination_folder)
        # Parse the HTML.
        soup = BeautifulSoup(response.text, "html.parser")
        # Download the HTML.
        with open(os.path.join(destination_folder, "index.html"), "w", encoding="utf-8") as html_file:
            html_file.write(str(soup))
        # Download images, CSS, and JS.
        for tag in soup.find_all(["img", "link", "script"]):
            if tag.has_attr("src") or tag.has_attr("href"):
                # Download the resource and save it in the destination folder.
                download_resource(urljoin(url, tag["src" if "src" in tag.attrs else "href"]), destination_folder)
        terminal("s", f"Download completed successfully in: {destination_folder}")
    else: terminal("e", f"Failed to access the URL. Status code: {response.status_code}")