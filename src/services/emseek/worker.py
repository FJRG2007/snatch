import re, ipaddress
from src.utils.basics import cls

from .services.domain.worker import main as mainDomainWorker
from .services.phone.worker import main as mainPhoneWorker
from .services.email.worker import main as mainEmailWorker
from .services.ip_address.worker import main as mainIpAddressWorker
from .services.username.worker import main as mainUserWorker

def main(input_data, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
    cls()
    if input_data == None or re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', input_data): mainEmailWorker(input_data, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list)
    elif re.match(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', input_data): mainDomainWorker(input_data)
    elif re.match(r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}', input_data): mainIpAddressWorker(ipaddress.ip_address(input_data)) 
    elif re.match(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', input_data): mainPhoneWorker(input_data) 
    else: mainUserWorker(input_data, saveonfile)