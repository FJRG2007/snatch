# Command: dirlist

**Description**: Verify the existence of vulnerable paths using dictionaries.

**Arguments**:
* `target` (required): Domain or IP address from where we will start listing the directories (do not include HTTP/S protocol).

**Options**:
* `-w` or `--wordlist` (optional): Dictionary with the routes to verify (by default Snatch includes its own).
* `-h` or `--hide` (optional): Codes to hide [default None, ex: 5XX or 5XX, 404].
* `--help` (optional): Display help information for the command.

> [!IMPORTANT]  
> If the whole list gives error, it is because the web has anti directory listing protections.

## Examples

The directories available in a domain/IP are listed.
```bash
# Listing Google directories with the default dictionary.
$ snatch dirlist google.com
# Listing Google directories with its own dictionary (Dicc in snatch/customs/directory_listing/my_dicc.txt).
$ snatch dirlist google.com -w my_dicc.txt
```

In this command we hide otuput that irelevants.
```bash
# When using 4XX it will not display errors in the range 400 - 499.
$ snatch dirlist google.com -h 4XX
# We can also specify a specific error.
$ snatch dirlist google.com -h "400, 404, 500" # or "4XX, 5XX"
```