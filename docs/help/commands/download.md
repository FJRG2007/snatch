# Command: dirlist

**Description**: Verify the existence of vulnerable paths using dictionaries.

**Arguments**:
* `target` (required): Domain or IP address from where we will start listing the directories (do not include HTTP/S protocol).

**Options**:
* `-w` or `--wordlist` (optional): Dictionary with the routes to verify (by default Snatch includes its own)..

> [!IMPORTANT]  
> If the whole list gives error, it is because the web has anti directory listing protections.

## Examples

This command will download everything found in that link including videos.
```bash
# Listing Google directories with the default dictionary.
$ snatch dir list google.com
# Listing Google directories with its own dictionary (Dicc in snatch/customs/directory_listing/my_dicc.txt).
$ snatch dir list google.com -w my_dicc.txt
```