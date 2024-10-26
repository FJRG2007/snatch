import time, random
from src.utils.basics import terminal
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

use_proxy = False # Set to True to use proxy, False to use your host IP.

if use_proxy: from seleniumwire import webdriver
else: from selenium import webdriver

def fetchsocks5():
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
    return f"socks5://{random.choice(proxies)}"

def fetchhttps():
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
    return f"https://{random.choice(proxies)}"

def fetchhttp():
    with open("proxies.txt") as f:
        proxies = f.read().splitlines()
    return f"http://{random.choice(proxies)}"

def search_on_pim_eyes(path, use_proxy):
    driver = None

    if use_proxy:
        prox = fetchsocks5() # FORMAT = USERNAME:PASS@IP:PORT
        options = {
            "proxy": {
                "http": prox,
                "https": prox,
                "no_proxy": "localhost,127.0.0.1"
            }
        }
        driver = webdriver.Chrome(seleniumwire_options=options)
    else:
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Uncomment to run Chrome in headless mode (no GUI).
        driver = webdriver.Chrome(options=chrome_options)
    
    results = None
    currenturl = None 

    try:
        driver.get("https://pimeyes.com/en")

        try: WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))).click()
        except Exception as e: terminal(f"Cookie consent button not found or not clickable: {e}")

        upload_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="hero-section"]/div/div[1]/div/div/div[1]/button[2]')))

        upload_button.click()
        
        file_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type=file]")))

        file_input.send_keys(path)
        # /html/body/div[6]/div/div/div/div/div/div/div[5]/div[1]/label/input
        agreement1_xpath = 'div.permissions > div:nth-child(1) > label > input[type=checkbox]'
        agreement2_xpath = 'div.permissions > div:nth-child(2) > label > input[type=checkbox]'
        agreement3_xpath = 'div.permissions > div:nth-child(3) > label > input[type=checkbox]'
        submit_xpath = '/html/body/div[6]/div/div/div/div/div/div/button'

        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, agreement1_xpath))).click()
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, agreement2_xpath))).click()
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, agreement3_xpath))).click()
        
        time.sleep(0.1)

        attempts = 0

        while attempts < 10:
            try:
                # Xpath to find the button with a span containing "Start Search".
                start_search_button_xpath = "//button[.//span[text()='Start Search']]"
                start_search_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, start_search_button_xpath)))
                start_search_button.click()
                print("Clicked 'Start Search' button successfully!")
                break # Exit the loop if clicked successfully.

            except Exception as e:
                print(f"'Start Search' button not clickable yet. Attempt {attempts + 1}/10. Retrying...")
                attempts += 1
                time.sleep(2) # Wait a bit before trying again.

        if attempts == 10:
            print("'Start Search' button is still not clickable after multiple attempts.")
            print("Attempting to submit the form by simulating Enter key...")
            form = driver.find_element(By.XPATH, "//form")
            form.click()
            form.send_keys(Keys.RETURN)

        time.sleep(5) # Give the page time to load results.
        currenturl = driver.current_url
        results = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="results"]/div/div/div[3]/div/div/div[1]/div/div[1]/button/div/span/span'))).text
    except Exception as e: print(f"An exception occurred: {e}")
    finally:
        print("Results: ", results)
        print("URL: ", currenturl)
        if driver: driver.quit()