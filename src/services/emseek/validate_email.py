import grequests
from .modules.skype import email2skype
from ...lib.data import requestsHeaders
from .modules.github import email2github
from .modules.aboutme import email2aboutme
from .modules.myspace import email2myspace
from .modules.twitter import twitter_search
from .modules.darksearch import dark_search
from .modules.linkedin import email2linkedin
from .modules.domaineye import email2domains
from .modules.gravatar import email2gravatar
from .modules.hibp_pastes import email_pastes
from .modules.googledork import google_search
from .modules.avast import email2breachedaccts

def validate_email(email):
	email_info={"email":email,"exists":False,"emailrep_limit_reached":False}
	accounts=[]
	sources=[]
	response = grequests.map([
		grequests.get(f"https://emailrep.io/{email}"),
		grequests.get(f"https://myspace.com/search/people?q={email}"),
		grequests.get(f'https://darksearch.io/api/search?query="{email}"'),
		grequests.get(f"https://api.github.com/search/users?q={email}+in:email"),
		grequests.post(f"https://digibody.avast.com/v1/web/leaks", json={"email": email}),
		grequests.get(f"https://haveibeenpwned.com/api/v2/pasteaccount/{email}", headers=requestsHeaders)
		
	])
	print(response)
	if response[0].status_code == 200:
		data = response[0].json()
		if (data["details"]["deliverable"] == True): email_info["exists"] = True
		if (data["details"]["last_seen"] != "never"): email_info["exists"] = True
		if (data["details"]["profiles"] != []):
			email_info["exists"]=True
			email_info["profiles"]=data["details"]["profiles"]
			if "gravatar" in email_info["profiles"]:
				gravatar = email2gravatar(email)
				if gravatar != []: accounts.extend(gravatar)
			if "aboutme" in email_info["profiles"]:
				aboutme = email2aboutme(email)
				if aboutme != []: accounts.extend(aboutme)
			if "linkedin" in email_info["profiles"]: accounts.append(email2linkedin(email))
		myspace = email2myspace(email,response[1])
		if (myspace != []):
			email_info["exists"] = True
			accounts.extend(myspace)
		github = email2github(email,response[2])
		if (github != ""):
			email_info["exists"] = True
			accounts.append(github)
		darksearch_sources = dark_search(email,response[3])
		if (darksearch_sources != []):
			email_info["exists"] = True
			sources.extend(darksearch_sources)
		pastes = email_pastes(email,response[4])
		if (pastes != []):
			email_info["exists"] = True
			email_info["pastes"] = pastes
		breached_accts = email2breachedaccts(email,response[5])
		if (breached_accts["accounts"] != []):
			email_info["exists"] = True
			accounts.extend(breached_accts["accounts"])
		if (breached_accts["breaches"] != []):
			email_info["exists"] = True
			email_info["breaches"] = breached_accts["breaches"]
		if (email_info["exists"] == True):
			skype = email2skype(email)
			if (skype != []): accounts.extend(skype)
			google_sources=google_search(email)
			if (google_sources != []): sources.extend(google_sources)
			twitter_sources=twitter_search(email)
			if (twitter_sources != []): sources.extend(twitter_sources)
			domains_registered = email2domains(email)
			if (domains_registered != []): email_info["domains_registered"] = domains_registered
		if accounts != []: email_info["accounts"] = accounts
		if sources != []: email_info["sources"] = sources
	else: email_info["emailrep_limit_reached"]=True
	return email_info