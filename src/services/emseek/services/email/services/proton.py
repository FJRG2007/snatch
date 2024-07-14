import re, requests
from datetime import datetime
from src.utils.basics import terminal

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def main(email):
    # Check if the protonmail exist : valid / not valid.
	bodyResponse = requests.get(f"https://api.protonmail.ch/pks/lookup?op=index&search={str(email)}").text
	if "info:1:0" in bodyResponse: print(f"Protonmail email is {bcolors.FAIL}not valid{bcolors.ENDC}")
	if  "info:1:1" in bodyResponse:
		print("Protonmail email is " + f"{bcolors.OKGREEN}valid{bcolors.ENDC}")
		regexPattern1 = "2048:(.*)::" #RSA 2048-bit (Older but faster)
		regexPattern2 = "4096:(.*)::" #RSA 4096-bit (Secure but slow)
		regexPattern3 = "22::(.*)::" #X25519 (Modern, fastest, secure)
		try:
			print("Date and time of the creation:", datetime.fromtimestamp(int(re.search(regexPattern1, bodyResponse).group(1))))
			print("Encryption : RSA 2048-bit (Older but faster)")
		except:
			try:
				print("Date and time of the creation:", datetime.fromtimestamp(int(re.search(regexPattern2, bodyResponse).group(1))))
				print("Encryption : RSA 4096-bit (Secure but slow)")
			except:
				print("Date and time of the creation:", datetime.fromtimestamp(int(re.search(regexPattern3, bodyResponse).group(1))))
				print("Encryption : X25519 (Modern, fastest, secure)")
		# Download the public key attached to the email.
		print(requests.get(f"https://api.protonmail.ch/pks/lookup?op=get&search={str(email)}").text)
	else: terminal("e", "There was an error verifying the email in Proton (Possibly: Many requests).")