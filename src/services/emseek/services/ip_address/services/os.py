import re, socket, subprocess
from scapy.all import sr1, IP, ICMP

def get_ttl(ip_address):
    try:
        # Execute the ping command to get the output.
        result = subprocess.run(["ping", "-c", "1", ip_address], capture_output=True, text=True)
        # Search TTL in the output of the ping command.
        ttl_match = re.search(r"ttl=(\d+)", result.stdout, re.IGNORECASE)
        if ttl_match: return { "success": True, "ttl": int(ttl_match.group(1)) }
        else: return { "success": False, "message": "TTL not found in ping response." }
    except Exception as e: return { "success": False, "message": f"Error retrieving TTL: {str(e)}" }

def is_port_open(ip_address, port):
    try:
        # Attempt to connect to the specified port.
        with socket.create_connection((ip_address, port), timeout=1) as sock:
            return True
    except Exception: return False

def get_os(ttl):
    try:
        if 0 <= ttl <= 64: return "GNU/Linux"
        elif 65 <= ttl <= 128: return "Microsoft Windows"
        else: return "Not Found"
    except Exception as e: return "Error determining OS"

async def get_os_main(ip_address):
    try:
        ttl_result = get_ttl(ip_address)
        if ttl_result["success"] and is_port_open(ip_address, 443): return get_os(ttl_result["ttl"])
        else: return "Not Found"
    except Exception as e: return "Error"

async def getOSName(ip):
    response = None
    try:
        if not ip: response = "Invalid IP"
        else: response = await get_os_main(ip)
    except Exception as e: response = "Error"
    return response
