import re
from .services.email.worker import main as mainEmailWorker
from .services.username.worker import main as mainUserWorker

def main(email_or_username, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
    if email_or_username == None or re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email_or_username): mainEmailWorker(email_or_username, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list)
    else: mainUserWorker(email_or_username, saveonfile)