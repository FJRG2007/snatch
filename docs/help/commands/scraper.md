# Command: scraper

**Description**: Advanced data extraction from social networks.

**Options**:
* `-p` or `--platforms` (optional): Platforms to scrape [all (default)...].
* `--userid` (optional): ID of the Discord user to investigate.
* `--intitle` (optional): Dorks: Search website by title.
* `--intext` (optional): Dorks: Search for content within a website.
* `--site` (optional): Dorks: Search website by domain.
* `--inurl` (optional): Dorks: Search website by path in url.
* `--filetype` (optional): Dorks: Search by file type.
* `--ext` (optional): Dorks: Search by extension type.

* `--numresults`, (optional): Dorks: Number of results to display (default 50).
* `-s` or `--saveonfile` (optional): Saves the information in a file.
* `--help` (optional): Display help information for the command.

## Examples

With this command a complete data extraction research is performed.
```bash
# Start a complete data extraction (all by default).
$ snatch scraper
# Start a complete extraction.
$ snatch scraper -p all
```

Extracting data from Discord.
```bash
# Data extraction from Discord (Snatch will ask for data).
$ snatch scraper -p discord
# Data extraction from Discord.
$ snatch scraper -p discord --userid "269617876036616193"
```

In this command, a search is performed on CIA public content using Google Dorks.
```bash
# Search for files from the domain "cia.gov" containing the word "confidential".
$ snatch scraper -p dorks --engine google --site cia.gov --intext "confidential"
```

### Supported platforms

* [x] Discord
* [x] Dorks -> Google.