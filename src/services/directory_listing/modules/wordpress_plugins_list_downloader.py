from bs4 import BeautifulSoup
import os, re, urllib.request as hyperlink

def download_plugins_list():
    response = hyperlink.urlopen("http://plugins.svn.wordpress.org/")
    page_content = response.read()
    decoded_content = page_content.decode("utf-8", errors="ignore")
    wordPressSoup = BeautifulSoup(decoded_content, "lxml")
    real_plugins = set()
    for line in wordPressSoup.get_text().splitlines():
        line = line.strip()
        if not line: continue
        line = re.sub(r"[\\\/]", "", line)
        line = re.sub(r"[^A-Za-z0-9._-]", "", line)
        if line: real_plugins.add(line)
    cleaned_lines = sorted(real_plugins)
    filePath = os.path.dirname(os.path.realpath(__file__))
    print(f"The current working directory of the file is {filePath} the scraped list has been saved.")
    with open("src/lib/files/directory_listing/wordpress/plugins.txt", "wt", encoding="utf8") as file:
        file.write("\n".join(cleaned_lines))