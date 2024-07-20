from selenium import webdriver
import os, time, math, datetime
from src.utils.basics import terminal
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException, InvalidArgumentException

class Logs():
    @staticmethod
    def create_log(username, logs_date):
        os.makedirs("output/whatsapp", exist_ok=True)
        with open("output/whatsapp/{} {}.txt".format(logs_date, username), "w") as f:
            f.write("Tracking to user {} has started at {}".format(username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "a"))

    @staticmethod
    def update_log(input, username, logs_date):
        with open("output/whatsapp/{} {}.txt".format(logs_date, username), "a") as f:
            f.write(f"\n{input}")
            f.close()

def study_user(driver, user, language):
	# First, go to their chat.
	try:
		# We instantiate our Logs class, save current date and create a text file for the user.
		logs = Logs()
		logs_date = datetime.datetime.now().strftime("%Y-%m-%d")
		logs.create_log(user, logs_date)
		terminal("s", f"There has been created in the folder \"output/whatsapp/\" a text file to log every connection and disconnection of the user {user}")
		
		x_arg = f"//span[contains(text(), \"{user}\")]"
		print(f"Trying to find: {x_arg}")
		driver.find_element(by=By.XPATH, value = x_arg).click()
		terminal("s", "Found and clicked.")
	except NoSuchElementException: return terminal("e", f"{user} is not found. Returning...")

	x_arg = str()
	# Now, we continuously check for their online status:
	if language == "en" or language == "de" or language == "pt": x_arg = "//span[@title=\"{}\"]".format("online")
	elif language == "es": x_arg = "//span[@title=\"{}\"]".format("en línea")
	elif language == "fr": x_arg = "//span[@title=\"{}\"]".format("en ligne")
	elif language == "cat": x_arg = "//span[@title=\"{}\"]".format("en línia")

	print("Trying to find: {} in user {}".format(x_arg, user))
	
	previous_state = "OFFLINE" # By default, we consider the user to be offline. The first time the user goes online.
	first_online = time.time()
	cumulative_session_time = 0
	# It will be printed.
	while True:
		try:
			driver.find_element(by=By.XPATH, value = x_arg)
			if previous_state == "OFFLINE":
				input = ("[{}][ONLINE] {}".format(
					datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
					user))
				print(input)
				logs.update_log(input, user, logs_date)	
				first_online = time.time()
				previous_state = "ONLINE"	
			
		except NoSuchElementException:
			if previous_state == "ONLINE":
			# Calculate approximate real time of WhatsApp being online.
				total_online_time = time.time() - first_online - 12 # approximately what it takes onPause to send signal.
				if total_online_time < 0: # This means that the user was typing instead of going offline.
					continue # Skip the rest of this iteration. Do nothing.
				cumulative_session_time += total_online_time
				input = ("[{}][DISCONNECTED] {} was online for {} seconds. Session total: {} seconds".format(
					datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
					user,
					math.floor(total_online_time),
					math.floor(cumulative_session_time)))
				print(input)
				logs.update_log(input, user, logs_date)	
				previous_state = "OFFLINE"
		except NoSuchWindowException: 
			terminal("e", "Your WhatsApp window has been minimized or closed, try running the code again, shutting down...")
			exit()
		time.sleep(1)

def whatsapp_login():
	try:
		print("In order to make this program to work, you will need to log-in once in WhatsApp. After that, your session will be saved until you revoke it.")
		options = webdriver.ChromeOptions()
		options.add_argument("user-data-dir=C:\\Path")
		options.add_experimental_option("excludeSwitches", ["enable-logging"])
		driver = webdriver.Chrome(options = options)
		if (os.getenv("WHATSAPP_AUTH_COOKIE") != ""):
			# Coming Soon.
			...
		else: driver.get("https://web.whatsapp.com")
		assert "WhatsApp" in driver.title 
		input("Press any key when you are at the chat menu...")
		return driver
	except InvalidArgumentException:
		terminal("e", "You may already have a Selenium navegator running in the background, close the window and run the code again, shutting down...")
		exit()

def main(username, language):
	if (language not in ["en", "es", "fr", "pt", "de", "cat"]): return terminal("e", "Enter a valid supported language -> en, es, fr, pt, de, cat.")
	try:	
		driver = whatsapp_login()
		study_user(driver, username, language)
	except KeyboardInterrupt:
		if driver: driver.quit()
		terminal(KeyboardInterrupt)