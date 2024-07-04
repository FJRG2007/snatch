import re
import os
import sys
import json
import pkg_resources
from ...utils.basics import terminal
from .validate_email import validate_email
from .gen_work_email import gen_work_email
from .gen_emails_from_info import gen_emails_from_info
from .gen_emails_from_pattern import gen_emails_from_pattern
from .basics import gen_emails_from_username

def print_info(email_info):
	if (email_info["exists"]==True):
		print("[+]" + email_info["email"])
		for i in email_info:
			if (i=="profiles"):
				print("\t[-]Profiles:")
				for profile in email_info["profiles"]:
					print("\t\t"+profile)
			elif (i=="sources"):
				print("\t[-]Sources:")
				for source in email_info["sources"]:
					print("\t\t"+source)
			elif (i=="accounts"):
				print("\t[-]Accounts:")
				for account in email_info["accounts"]:
					print("\t\t"+account)
			elif (i=="twitter"):
				print("\t"+email_info["twitter"])
			elif (i=="domains_registered"):
				print("\t[-]Domains registered:")
				for domain in email_info["domains_registered"]:
					print("\t\t"+domain)
			elif (i=="phone_number"):
				print("\t[-]Phone Number:")
				print("\t"+email_info["phone_number"])
			elif (i=="position"):
				print("\t[-]Position:")
				print("\t"+email_info["position"])
			elif (i=="breaches"):
				print("\t[-]Breaches:")
				for breach in email_info["breaches"]:
					print("\t\t"+breach)
			elif (i=="pastes"):
				print("\t[-]Pastes:")
				for paste in email_info["pastes"]:
					print("\t\t"+paste)

def main(email, first, middle, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
	if (saveonfile):
		if not os.path.exists("output/emseek"): os.makedirs("output/emseek")
		sys.stdout = open(f"output/emseek/{email}", 'w+')
	
	if (email and first and middle and last and birthdate and('*' in email)):
		if addinfo: input_info={"first":[first],"middle":[middle],"last":[last],"birthdate":[birthdate],"additional_info":addinfo}
		else: input_info={"first":[first],"middle":[middle],"last":[last],"birthdate":[birthdate]}
		generated_emails=gen_emails_from_pattern(input_info,email)
		if (generated_emails != []):
			print(f"[=]Validating {str(len(generated_emails))} possible emails.")
			for email in generated_emails:
				email_info = validate_email(email)
				if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
				else:
					print("[=]You have reached your daily limit")
					exit(1)

	elif (email and first and middle and last and('*' in email)):
		if addinfo: input_info={"first":[first],"middle":[middle],"last":[last],"additional_info":addinfo}
		else: input_info={"first":[first],"middle":[middle],"last":[last]}
		generated_emails=gen_emails_from_pattern(input_info,email)

		if (generated_emails != []):
			print(f"[=]Validating {str(len(generated_emails))} possible emails.")
			for email in generated_emails:
				email_info = validate_email(email)
				if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
				else:
					print("[=]You have reached your daily limit")
					exit(1)


	elif (email and first and last and birthdate and('*' in email)):
		if addinfo: input_info={"first":[first],"last":[last],"birthdate":[birthdate],"additional_info":addinfo}
		else: input_info={"first":[first],"last":[last],"birthdate":[birthdate]}
		generated_emails=gen_emails_from_pattern(input_info,email)
		if (generated_emails != []):
			print(f"[=]Validating {str(len(generated_emails))} possible emails.")
			for email in generated_emails:
				email_info = validate_email(email)
				if (email_info["emailrep_limit_reached"] == False):
					print_info(email_info)
				else:
					print("[=]You have reached your daily limit")
					exit(1)


	elif (email and first and last):
		if addinfo: input_info = {"first": [first],"last": [last], "additional_info": addinfo}
		else: input_info = {"first": [first], "last": [last]}
	
		generated_emails = gen_emails_from_pattern(input_info,email)
	
		print(f"[=]Validating {str(len(generated_emails))} possible emails.")
		if (generated_emails != []):
			for email in generated_emails:
				email_info = validate_email(email)
				if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
				else:
					print("[=]You have reached your daily limit")
					exit(1)


	elif (email and ('*' not in email)):
		email_info = validate_email(email)
		if (email_info["emailrep_limit_reached"] == False and email_info["exists"] == True): print_info(email_info)
		elif (email_info["emailrep_limit_reached"] == False and email_info["exists"] == False): print(f"[=]No Info was found on the email address {email}")
		else:
			print("[=]You have reached your daily limit")
			exit(1)

	elif (first and last and company):
		email_info = gen_work_email(first,last,company)
		if ("hunter_limit_reached" in email_info):
			print("[=]Error:You have reached your Hunter.io usage limit")
			print("[=]Use an API key if you want to use this option")
		else:
			if (email_info["emailrep_limit_reached"] == False and email_info["exists"] == True): print_info(email_info)
			elif (email_info["emailrep_limit_reached"] == True):
				print("[=]You have reached your daily limit.")
				exit(1)
			elif (email_info["exists"] == False): print("[=]We were unable to find a person with this name working for this company.")


	elif (first and middle and last and birthdate):
		input_info = {"first": first, "middle": middle, "last": last, "birthdate": birthdate}
		if (providers):
			generated_emails=gen_emails_from_info(input_info,providers)
			if (validate):
				for email in generated_emails:
					email_info = validate_email(email)
					if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
					else:
						print("[=]You have reached your daily limit.")
						exit(1)
			else:
				print("[=]Generated emails:")
				for email in generated_emails:
					print(email + "\n")
		else:
			generated_usernames=gen_emails_from_info(input_info,[])
			print("[=]Generated usernames:")
			for username in generated_usernames:
				print(username + "\n")


	elif (first and middle and last):
		input_info={"first":first,"middle":middle,"last":last}
		if (providers):
			generated_emails=gen_emails_from_info(input_info,providers)
			if (validate):
				for email in generated_emails:
					email_info = validate_email(email)
					if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
					else:
						print("[=]You have reached your daily limit")
						exit(1)
			else:
				print("[=]Generated emails:")
				for email in generated_emails:
					print(email + "\n")
		else:
			generated_usernames=gen_emails_from_info(input_info,[])
			print("[=]Generated usernames:")
			for username in generated_usernames:
				print(username + "\n")


	elif (first and last and birthdate):
		input_info = {"first": first, "last": last, "birthdate": birthdate}
		if (providers):
			generated_emails = gen_emails_from_info(input_info,providers)
			if (validate):
				for email in generated_emails:
					email_info = validate_email(email)
					if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
					else:
						print("[=]You have reached your daily limit.")
						exit(1)
			else:
				print("[=]Generated emails:")
				for email in generated_emails:
					print(email + "\n")
		else:
			generated_usernames = gen_emails_from_info(input_info,[])
			print("[=]Generated usernames:")
			for username in generated_usernames:
				print(username + "\n")


	elif (first and last):
		input_info = {"first": first, "last": last}
		if (providers):
			generated_emails = gen_emails_from_info(input_info,providers)
			if (validate):
				for email in generated_emails:
					email_info = validate_email(email)
					if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
					else:
						print("[=]You have reached your daily limit")
						exit(1)
			else:
				print("[=]Generated emails:")
				for email in generated_emails:
					print(email + "\n")
		else:
			generated_usernames = gen_emails_from_info(input_info,[])
			print("[=]Generated usernames:")
			for username in generated_usernames:
				print(username + "\n")

	

	elif (username and providers):
		generated_emails = gen_emails_from_username(username,providers)
		if (generated_emails != []):
			print(f"[=]Validating {str(len(generated_emails))} possible emails.")
			for email in generated_emails:
				email_info = validate_email(email)
				if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
				else:
					print("[=]You have reached your daily limit.")
					exit(1)
			
	elif (username):
		domain_list=[]		
		with open( pkg_resources.resource_filename('data', 'email-providers.json'),'r') as json_file:
			domains = json.loads(json_file.read())
			for domain in domains:
				domain_list.append(domain)

		generated_emails=gen_emails_from_username(username,domain_list)
		if (generated_emails != []):
			print(f"[=]Validating {str(len(generated_emails))} possible emails.")
			for email in generated_emails:
				email_info = validate_email(email)
				if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
				else:
					print("[=]You have reached your daily limit")
					exit(1)

	elif (list):
		with open(list,'r') as f:
			emails = f.readlines()
			emails = [x.rstrip() for x in emails]
		for email in emails:
			if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$', email) != None:
				email_info = validate_email(email)
				if (email_info["emailrep_limit_reached"] == False): print_info(email_info)
				else:
					print("[=]You have reached your daily limit")
					exit(1)
	else: print_info(email_info)