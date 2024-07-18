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

Scans all ports of a domain.
```bash
# Scans all ports of a domain (all ports by default).
$ snatch portscan example.com
# Specified, scan all ports.
$ snatch portscan example.com -p "*"
```

Scans the common ports of a domain.
```bash
$ snatch portscan example.com -p common
```

Scan ports 80 and 443.
```bash
$ snatch portscan example.com -p "80, 443"
```

Scan ports by ranges
```bash
# Scan first 300 ports.
$ snatch portscan example.com -p "*-300"

# Scans all ports from 30000 and upwards. We set twice as many threads by default, to go faster.
$ snatch portscan example.com -p "30000-*" -t 100

# Scans ports 80 to 443.
$ snatch portscan example.com -p "80-443"
```