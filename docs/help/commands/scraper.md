# Command: scraper

**Description**: Advanced data extraction from social networks.

**Options**:
* `-p` or `--platforms` (optional): Platforms to scrape [all (default)...].
* `--dscuserid` (optional): ID of the Discord user to investigate.
* `--help` (optional): Display help information for the command.

## Examples

With this command a complete data extraction research is performed.
```bash
# Start a complete data extraction (all by default).
$ snatch scraper
# Start a complete extraction.
$ snatch scraper -p all
```

Extracting data from Discord
```bash
# Data extraction from Discord (Snatch will ask for data).
$ snatch scraper -p discord
# Data extraction from Discord.
$ snatch scraper -p discord --dscuserid "269617876036616193"
```

### Supported platforms

* [x] Discord