# Command: portscan

**Description**: Mass port scanning.

**Arguments**:
* `target` (required): Domain or IP address from where we will start scanning ports (do not include HTTP/S protocol).

**Options**:
* `-p` or `--ports` (optional): Ports to be scanned (1,2,3 or 16-24 or \*-24 or 24-\* or * or common).
* `-t` or `--threads` (optional): Number of simultaneous threads for the requests (default 50).
* `-s` or `--saveonfile` (optional): Saves the open ports in a file.
* `--help` (optional): Display help information for the command.

## Examples

> [!IMPORTANT]  
> For demonstration purposes, only the ports on the user's local machine will be scanned. Scanning ports on external machines might not be legal or appropriate.

Scans all ports of a domain.
```bash
# Scans all ports of a domain (all ports by default).
$ snatch portscan localhost
# Specified, scan all ports.
$ snatch portscan localhost -p "*"
```

Scans the common ports of a domain.
```bash
$ snatch portscan localhost -p common
```

Scan ports 80 and 443.
```bash
$ snatch portscan localhost -p "80, 443"
```

Scan ports by ranges
```bash
# Scan first 300 ports.
$ snatch portscan localhost -p "*-300"

# Scans all ports from 30000 and upwards. We set twice as many threads by default, to go faster.
$ snatch portscan localhost -p "30000-*" -t 1000

# Scans ports 80 to 443.
$ snatch portscan localhost -p "80-443"
```