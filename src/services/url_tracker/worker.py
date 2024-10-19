import time, socket, requests
from src.utils.basics import terminal

def main(url):
    try:
        session = requests.Session()
        start_time = time.time()
        response = session.get(url, allow_redirects=True)
        total_time = time.time() - start_time

        history = response.history
        if history:
            print(f"Tracking URL: {url}")
            print(f"Total redirects: {len(history)}")
            for i, res in enumerate(history, 1):
                print(f"Redirect {i}:")
                print(f" - URL: {res.url}")
                print(f" - Status Code: {res.status_code}")
                print(f" - Time Elapsed: {res.elapsed.total_seconds()}s")
        final_ip = socket.gethostbyname(response.url.split("//")[-1].split("/")[0])
        print("\nFinal URL Information:")
        print(f" - Final URL: {response.url}")
        print(f" - Status Code: {response.status_code}")
        print(f" - Response Time: {total_time:.4f}s")
        print(f" - Content Type: {response.headers.get('Content-Type')}")
        print(f" - IP Address: {final_ip}")
        print(f" - Response Content (first 500 chars): {response.text[:500]}")
    except requests.exceptions.RequestException as e: terminal("e", f"Error tracking URL: {e}")