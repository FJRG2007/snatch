# Command: whatsapp

**Description**: Generates basic logs of user activity in WhatsApp.

**Arguments**:
* `username` (required): Contact name to be scraped.
* `language` (required): WhatsApp language (only supported [en, es, fr, pt, de, cat]).

**Options**:
* `--help` (optional): Display help information for the command.

> [!NOTE]  
> If the user's status is disabled, it will not be possible to scrape it.

## Examples

Here you start scraping the status of the `girlfriend` contact.
```bash
$ snatch whatsapp "girlfriend" en
```