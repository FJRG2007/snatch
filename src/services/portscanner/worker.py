import os
import sys
import socket
import src.lib.colors as cl
import src.lib.data as data
from datetime import datetime
from ...utils.basics import terminal
from threading import Thread, Semaphore

class InvalidPortException(Exception):
    pass

def parse_ports(port_str):
    ports = set()
    port_str = port_str.replace(" ", "")
    if port_str == "*": return list(range(1, 65536))
    elif port_str == "common": return [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 5900, 8080, 8443]
    ranges = port_str.split(",")
    for part in ranges:
        if "-" in part:
            start, end = part.split("-")
            try:
                if start == "*": start = 1
                else: start = int(start)
                if end == "*": end = 65535
                else: end = int(end)
                if start > end: raise InvalidPortException(f"Invalid port range: {part}")
                ports.update(range(start, end + 1))
            except ValueError: raise InvalidPortException(f"Invalid port range: {part}")
        else:
            try: ports.add(int(part))
            except ValueError: raise InvalidPortException(f"Invalid port range: {part}")
    return sorted(ports)

def main(target, ports, threadsNumber=10, saveonfile=False):
    # Add Banner.
    print(f"{cl.des_space}" + "-" * 50)
    print(f"{cl.des_space}Scanning Target: {target}")
    print(f"{cl.des_space}Scanning ports: {'All (65535)' if ports == '*' else ports.capitalize()}")
    print(f"{cl.des_space}Scanning started at: {str(datetime.now())}")
    print(f"{cl.des_space}Number of threads: {threadsNumber}")
    print(f"{cl.des_space}" + "-" * 50 + "\n")
    if not isinstance(threadsNumber, int) or threadsNumber < 1 or threadsNumber > 9999: return terminal("e", "Set a valid number of threads between 1 and 9999.")
    # Semaphore to limit the number of simultaneously active threads.
    semaphore = Semaphore(threadsNumber)
    open_ports = []

    def scan_ports(ports_to_scan, thread_id):
        nonlocal open_ports
        try:
            for port in ports_to_scan:
                semaphore.acquire()  # Acquire the semaphore.
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"{cl.G} T-{thread_id:04} {cl.w} Open port {port}.")
                s.close()
                semaphore.release()  # Releasing the semaphore after port scanning.
        except KeyboardInterrupt:
            terminal("e", KeyboardInterrupt)
            sys.exit()
        except socket.gaierror:
            terminal("e", "Hostname Could Not Be Resolved.")
            sys.exit()
        except socket.error:
            terminal("e", "Server not responding.")
            sys.exit()

    # Validating and preparing the ports to be scanned.
    try:
        ports = parse_ports(ports)
    except InvalidPortException as e:
        terminal("e", e)
        print(f"Example: {data.pre_cmd} portscan example.com or ip --ports 1,2,3 or 16-24 or *-24 or 24-* or * or common")
        sys.exit(1)

    # Distribute the ports among the threads.
    ports_per_thread = len(ports) // threadsNumber
    threads = []
    for i in range(threadsNumber):
        start = i * ports_per_thread
        thread_ports = ports[start:start + ports_per_thread if i != threadsNumber - 1 else len(ports)]
        thread = Thread(target=scan_ports, args=(thread_ports, i+1))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish.
    for thread in threads:
        thread.join()

    if saveonfile:
        os.makedirs("portscans", exist_ok=True)
        filename = f"output/portscans/{target.replace('.', '_')}_open_ports.txt"
        with open(filename, "w") as f:
            f.write(",".join(map(str, open_ports)))
        terminal("s", f"Open ports have been saved to {filename}.")
    else: return open_ports