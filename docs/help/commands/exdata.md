# Command: exdata

**Description**: Extracts metadata information from files.

**Options**:
* `-t` or `--tool` (optional): Use an advanced tool [exiftool (default), snatch].
* `-s` or `--saveonfile` (optional): Saves the information in a file.
* `--help` (optional): Display help information for the command.

## Examples

Here, you can extract the metadata from the files in the `custom/extract_metadata` folder.
```bash
# All metadata is extracted using exiftool by default.
$ snatch exdata
```