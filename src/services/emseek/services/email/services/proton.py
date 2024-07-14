import re, requests, ipaddress
from datetime import datetime
from src.utils.basics import cls, noToken, terminal, setColor, getTypeString

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def checkProtonAPIStatut():
	requestProton_mail_statut = requests.get('https://api.protonmail.ch/pks/lookup?op=index&search=test@protonmail.com')
	if requestProton_mail_statut.status_code == 200: print("Protonmail API is " + f"{bcolors.BOLD}ONLINE{bcolors.ENDC}")
	else: print("Protonmail API is " + f"{bcolors.BOLD}OFFLINE{bcolors.ENDC}")

	requestProton_vpn_statut = requests.get('https://api.protonmail.ch/vpn/logicals')
	if requestProton_vpn_statut.status_code == 200: print("Protonmail VPN is " + f"{bcolors.BOLD}ONLINE{bcolors.ENDC}")
	else: print("Protonmail VPN is " + f"{bcolors.BOLD}OFFLINE{bcolors.ENDC}")

def checkValidityOneAccount(email, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
	# Test the validity of one protonmail account.
	
	print("You want to know if a protonmail email is real ?")

	#Check if the protonmail exist : valid / not valid
	bodyResponse = requests.get(f"https://api.protonmail.ch/pks/lookup?op=index&search={str(email)}").text
	
	protonNoExist = "info:1:0" #not valid
	protonExist = "info:1:1" #valid

	if protonNoExist in bodyResponse: print("Protonmail email is " + f"{bcolors.FAIL}not valid{bcolors.ENDC}")

	if protonExist in bodyResponse:
		print("Protonmail email is " + f"{bcolors.OKGREEN}valid{bcolors.ENDC}")
		regexPattern1 = "2048:(.*)::" #RSA 2048-bit (Older but faster)
		regexPattern2 = "4096:(.*)::" #RSA 4096-bit (Secure but slow)
		regexPattern3 = "22::(.*)::" #X25519 (Modern, fastest, secure)
		try:
			timestamp = int(re.search(regexPattern1, bodyResponse).group(1))
			dtObject = datetime.fromtimestamp(timestamp)
			print("Date and time of the creation:", dtObject)
			print("Encryption : RSA 2048-bit (Older but faster)")
		except:
			try:
				timestamp = int(re.search(regexPattern2, bodyResponse).group(1))
				dtObject = datetime.fromtimestamp(timestamp)
				print("Date and time of the creation:", dtObject)
				print("Encryption : RSA 4096-bit (Secure but slow)")
			except:
				timestamp = int(re.search(regexPattern3, bodyResponse).group(1))
				dtObject = datetime.fromtimestamp(timestamp)
				print("Date and time of the creation:", dtObject)
				print("Encryption : X25519 (Modern, fastest, secure)")

		# Download the public key attached to the email.
		print(requests.get(f"https://api.protonmail.ch/pks/lookup?op=get&search={str(email)}").text)

# Try to find if your target has a protonmail account by generating multiple addresses by combining information fields inputted.
def checkGeneratedProtonAccounts(email, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
    if not name or not first or not last: return terminal("e", "You must define your target's first and last name.")
    if not birthdate: birthdate = ""
    # Protonmail domain
    domainList = ["@protonmail.com", "@proton.me", "@protonmail.ch", "@pm.me"]
    # List of combinations.
    pseudoList = []
    
    for domain in domainList:
        # For domain.
        pseudoList.append(first + last + domain)
        pseudoList.append(first + last + name + domain)
        pseudoList.append(name[0] + first + last + domain)
        pseudoList.append(username + domain)
        pseudoList.append(addinfo + domain)
        pseudoList.append(first + last + domain)
        pseudoList.append(name + first + last + birthdate + domain)
        pseudoList.append(name[0] + first + last + birthdate + domain)
        pseudoList.append(first + last + name + birthdate + domain)
        pseudoList.append(username + birthdate + domain)
        pseudoList.append(addinfo + birthdate + domain)
        pseudoList.append(name + first + last + birthdate[-2:] + domain)
        pseudoList.append(name + first + last + birthdate[-2:] + domain)
        pseudoList.append(name[0] + first + last + birthdate[-2:] + domain)
        pseudoList.append(first + last + name + birthdate[-2:] + domain)
        pseudoList.append(username + birthdate[-2:] + domain)
        pseudoList.append(addinfo + birthdate[-2:] + domain)

    # Remove duplicates from list.
    pseudoListUniq = []
    for i in pseudoList:
        if i not in pseudoListUniq: pseudoListUniq.append(i)

    # Remove all irrelevant combinations.
    for domain in domainList:
        if domain in pseudoListUniq: pseudoListUniq.remove(domain)
        if birthdate + domain in pseudoListUniq: pseudoListUniq.remove(birthdate + domain)
        if birthdate[-2:] + domain in pseudoListUniq: pseudoListUniq.remove(birthdate[-2:] + domain)
        if name + domain in pseudoListUniq: pseudoListUniq.remove(name + domain)

    print(f"I'm trying some combinations: {str(len(pseudoListUniq))}")

    for pseudo in pseudoListUniq:
        requestProton = requests.get(f'https://api.protonmail.ch/pks/lookup?op=index&search={pseudo}').text
        protonNoExist = "info:1:0"  # Not valid.
        protonExist = "info:1:1"  # Valid.
        if protonNoExist in requestProton: print(pseudo + " is " + f"{bcolors.FAIL}not valid{bcolors.ENDC}")

        if protonExist in requestProton:
            regexPattern1 = "2048:(.*)::"
            regexPattern2 = "4096:(.*)::"
            regexPattern3 = "22::(.*)::"
            try:
                timestamp = int(re.search(regexPattern1, requestProton).group(1))
                dtObject = datetime.fromtimestamp(timestamp)
                print(pseudo + " is " + f"{bcolors.OKGREEN}valid{bcolors.ENDC}" + " - Creation date:", dtObject)
            except AttributeError: continue
            except:
                try:
                    timestamp = int(re.search(regexPattern2, requestProton).group(1))
                    dtObject = datetime.fromtimestamp(timestamp)
                    print(pseudo + " is " + f"{bcolors.OKGREEN}valid{bcolors.ENDC}" + " - Creation date:", dtObject)
                except AttributeError: continue
                except:
                    timestamp = int(re.search(regexPattern3, requestProton).group(1))
                    dtObject = datetime.fromtimestamp(timestamp)
                    print(pseudo + " is " + f"{bcolors.OKGREEN}valid{bcolors.ENDC}" + " - Creation date:", dtObject)

def main(email, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
    checkValidityOneAccount(email, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list)
    checkGeneratedProtonAccounts(email, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list)