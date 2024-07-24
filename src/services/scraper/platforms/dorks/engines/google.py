from __future__ import print_function
from src.utils.basics import terminal, fileManager
import random
from time import sleep
from requests import get
from bs4 import BeautifulSoup

def _req(term, results, lang, start, proxies, timeout, safe, ssl_verify):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": random.choice([
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
])
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests.
            "hl": lang,
            "start": start,
            "safe": safe,
        },
        proxies=proxies,
        timeout=timeout,
        verify=ssl_verify,
    )
    resp.raise_for_status()
    return resp

class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"

def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5, safe="active", ssl_verify=None):
    # Proxy setup.
    proxies = {"https": proxy} if proxy and proxy.startswith("https") else {"http": proxy} if proxy else None
    start = 0
    fetched_results = 0  # Keep track of the total fetched results.
    while fetched_results < num_results:
        # Send request.
        resp = _req(term.replace(" ", "+"), num_results, lang, start, proxies, timeout, safe, ssl_verify)
        # Parse.
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        new_results = 0  # Keep track of new results in this iteration.
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find("div", {"style": "-webkit-line-clamp:2"})
            if link and title and description_box:
                description = description_box.text
                fetched_results += 1
                new_results += 1
                if advanced: yield SearchResult(link["href"], title.text, description)
                else: yield link["href"]
            if fetched_results >= num_results: break  # Stop if we have fetched the desired number of results
        if new_results == 0: break  # Break the loop if no new results were found in this iteration.
        start += 10  # Prepare for the next set of results.
        sleep(sleep_interval)

def logger(data, namefile):
    file = open(f"{namefile}.txt", "a")
    file.write(str(data))
    file.write("\n")
    file.close()

def main(query, num_results, saveonfile):
    # To construct the query for dorking.
    formatted_query = ""
    for key, value in query.items():
        if value: formatted_query += f'{key}:"{value}" '
    formatted_query = formatted_query.strip()
    if not formatted_query: return terminal("e", "Please specify a query.", exitScript=True)
    try:
        requ = 0
        counter = 0
        for results in search(formatted_query, num_results, lang="en"):
            counter = counter + 1
            print("[+] ", counter, results)
            sleep(0.1)
            requ += 1
            if requ >= num_results: break
            if saveonfile:
                file = open(fileManager("scraper", f"dorks_engine_google_{query}.txt"), "a")
                file.write(str((counter, results)))
                file.write("\n")
                file.close()
            sleep(0.1)
    except KeyboardInterrupt: terminal(KeyboardInterrupt)
    except Exception as e: pass