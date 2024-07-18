# Command: download

**Description**: Easily download content from the Internet.

**Arguments**:
* `url` (optional): Url from where to download the content. If it is not defined, it will go to the configuration file `customs/snatch/downloads.json`.

**Options**:
* `-d` or `--dtype` (optional): Download type [source (default), video, audio...].
* `-f` or `--format` (optional): In case of reloading a resource, choose the format.
* `--help` (optional): Display help information for the command.

## Examples

This command will download everything found in that link including videos.
```bash
# Downloading all content linked to a URL.
$ snatch download https://www.youtube.com/watch?v=7PAk1wsy3VI
# Or (technically correct option).
$ snatch download "https://www.youtube.com/watch?v=7PAk1wsy3VI"
```

In this mode, you ask questions directly to Snatch without going through the prompt "interface".
```bash
# Downloading a video in mp4 format (default) from Snatch supported websites.
$ snatch download https://www.youtube.com/watch?v=7PAk1wsy3VI -d video
# Downloading a playlist in mp3 format from Snatch supported websites.
$ snatch download https://www.youtube.com/watch?v=qW96515QG6Y&list=PLrFPX1Vfqk3ehZKSFeb9pVIHqxqrNW8Sy -d video -f mp3
```

### Supported websites for "native" download

> [!NOTE]  
> If the website is not a native download in Snatch, then only public files accessible from the provided URL will be downloaded.

* [x] X/Twitter
* [x] YouTube