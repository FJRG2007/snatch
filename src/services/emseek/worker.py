import re
from .search_email import search_email
from .search_username import search_username

def main(email_or_username, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
    if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email_or_username): search_email(email_or_username, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list)
    else: search_username(email_or_username, saveonfile)