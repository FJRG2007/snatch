# Command: emseek

**Description**: Extracts and validates data such as emails, usernames, domains, phone numbers, ips, etc.

**Arguments**:
* `input_data` (optional): Domain/email/username/phone/ip you want to extract information from.

**Options**:
* `-n` or `--name` (optional): Name of person to extract information.
* `-f` or `--first` (optional): First surname of the person to extract information.
* `-l` or `--last` (optional): Second last name of the person to extract information.
* `-b` or `--birthdate` (optional): Birthday of the person to be extracted information, if you dont know(ex:****1967,3104****).
* `-a` or `--addinfo` (optional): Additional/concrete information you know about the victim (ex:king,345981).
* `-u` or `--username` (optional): Possible victim's username.
* `-c` or `--company` (optional): Company where the victim works or has worked.
* `-p` or `--providers` (optional): Email provider used by the victim.
* `-s` or `--saveonfile` (optional): Saves the information in a file.
* `-v` or `--validate` (optional): Check which emails/other inputs are valid and returns information of each one.
* `--datalist` (optional): File containing list of emails.
* `--help` (optional): Display help information for the command.

> [!IMPORTANT]
> Emeseek works and extracts more data as more APIs are connected.

## Examples

In this command, information is searched for that user.
```bash
# Search for emails or social network accounts with that user.
$ snatch emseek fjrg2007
```

Here are data extracted from Google.
```bash
# Extract data from a domain.
$ snatch emseek google.com
```