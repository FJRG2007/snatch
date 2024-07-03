import sys
import socket
import src.lib.data as data
from datetime import datetime
from rich import print as rprint

class InvalidPortException(Exception):
    pass

def parse_ports(port_str):
    ports = set()
    port_str = port_str.replace(" ", "")
    
    if port_str == "*": return set(range(1, 65536))
    
    ranges = port_str.split(",")
    
    for part in ranges:
        if "-" in part:
            start, end = part.split("-")
            try:
                if start == "*":  start = 1
                else: start = int(start)
                
                if end == "*": end = 65535
                else: end = int(end)

                if start > end: raise InvalidPortException(f"Invalid port range: {part}")
                
                ports.update(range(start, end + 1))
            except ValueError: raise InvalidPortException(f"Invalid port range: {part}")
        else:
            try: ports.add(int(part))
            except ValueError: raise InvalidPortException(f"Invalid port range: {part}")
                
    return ports

def main(target, ports):
    try:
        # Validating and preparing the ports to be scanned.
        ports = parse_ports(ports)
    except InvalidPortException as e:
        rprint(f"[red]Error: {e}[/red]")
        print(f"Example: {data.pre_cmd} portscan example.com or ip --ports 1,2,3 or 16-24 or *-24 or 24-* or *")
        sys.exit(1)

    # Add Banner.
    print("-" * 50)
    print(f"Scanning Target: {target}")
    print(f"Scanning started at: {str(datetime.now())}")
    print("-" * 50)

    try:
     
    # Will scan ports between 1 to 65535.
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
         
            # Returns an error indicator.
            result = s.connect_ex((target, port))
            if result ==0:
                print("Port {} is open".format(port))
            s.close()
         
    except KeyboardInterrupt:
            rprint("[red]Exiting Program: Canceled by user.[/red]")
            sys.exit()
    except socket.gaierror:
            rprint("[red]Error: Hostname Could Not Be Resolved.[/red]")
            sys.exit()
    except socket.error:
            rprint("[red]Error: Server not responding.[/red]")
            sys.exit()