import random
import requests
from os import getenv
from .validate_email import validate_email

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


# Generate work email from first name,last name and company domain.
# Returns the email with information associated to it.

def gen_work_email(first,last,domain):
	useragents = [
			'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17',
			'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
			'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
			'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0',
			'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
			'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
			'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
	]
	headers={'User-Agent':random.choice(useragents)}

	work_email_info={}
	api_key = getenv("HUNTER_API_KEY")
	baseUrl = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first}&last_name={last}"
	if api_key == "": response = requests.get(baseUrl, headers = headers)
	else: response= requests.get(baseUrl+ "&api_key=" + api_key)
	
	if response.status_code == 200:
		data = response.json()
		work_email=data["data"]["email"]
		if (data["data"]["position"] != ""): work_email_info["position"]=data["data"]["position"]
		if (data["data"]["twitter"] != ""): work_email_info["twitter"]="https://www.twitter.com/" + data["data"]["twitter"]
		if (data["data"]["phone_number"] != ""): work_email_info["phone_number"]=data["data"]["phone_number"]
		info=merge_two_dicts(work_email_info,validate_email(work_email))
	else: info={"hunter_limit_reached": True}
	return info