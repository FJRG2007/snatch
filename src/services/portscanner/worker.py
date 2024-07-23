import src.lib.colors as cl
import src.lib.data as data
from statistics import mean
from datetime import datetime
import os, sys, socket, subprocess
from src.utils.basics import terminal
from threading import Thread, Semaphore

class InvalidPortException(Exception): pass

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

def main(target, ports, threadsNumber=50, saveonfile=False):
    # Add Banner.
    print("-" * 50)
    print(f"Scanning target: {target}")
    print(f"Scanning ports: {'All (65535)' if ports == '*' else ports.capitalize()}")
    print(f"Scanning started at: {str(datetime.now())}")
    print(f"Number of threads: {threadsNumber}")
    print("-" * 50 + f"\n{cl.w}")
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
                s.settimeout(timeout)
                result = s.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"{cl.G} T-{thread_id:04} {cl.w} Open port {port}.")
                s.close()
                semaphore.release()  # Releasing the semaphore after port scanning.
        except KeyboardInterrupt: terminal("e", KeyboardInterrupt)
        except socket.gaierror: terminal("e", "Hostname Could Not Be Resolved.")
        except socket.error: terminal("e", "Server not responding.")

    def ping_avg_time(target):
        try:
            output = subprocess.check_output(['ping', '-c', '3', target])
            times = []
            for line in output.decode('utf-8').splitlines():
                if "time=" in line: times.append(float(line.split("time=")[-1].split(" ")[0]))
            return mean(times) if times else 0.0
        except subprocess.CalledProcessError: return 0.0
        except Exception as e:
            terminal("e", f"Error while pinging {target}: {e}")
            return 0.0
    # Validating and preparing the ports to be scanned.
    try: ports = parse_ports(ports)
    except InvalidPortException as e:
        terminal("e", e)
        print(f"Example: {data.pre_cmd} portscan example.com or ip --ports 1,2,3 or 16-24 or *-24 or 24-* or * or common")
        sys.exit(1)
    ping_time = ping_avg_time(target)
    if ping_time > 0: timeout = ping_time * 1.6  # Use twice the average ping time as the initial wait time.
    else: timeout = 0.5  # Default value if ping time cannot be obtained.

    # Distribute the ports among the threads.
    ports_per_thread = len(ports) // threadsNumber
    remaining_ports = len(ports) % threadsNumber
    threads = []

    start = 0
    for i in range(threadsNumber):
        extra = 1 if i < remaining_ports else 0
        end = start + ports_per_thread + extra
        thread_ports = ports[start:end]
        start = end
        thread = Thread(target=scan_ports, args=(thread_ports, i + 1))
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