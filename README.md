# Wikifeet Image Downloader

A lightweight Python utility for downloading all publicly available images from supported Wikifeet and WikifeetX model pages.

This project was inspired by an existing downloader but has evolved into its own implementation with numerous improvements and additional features.

Some of these improvements were shared with the original maintainer, who responded positively and intended to integrate them in the future. Since the original project has not seen further development for quite some time, this standalone version was created so the work can continue instead of remaining unused.

## Features

- Download all available images from a model page
- Skip already downloaded files
- Parallel downloads
- Automatic retry handling
- Configurable request timeout and retry delay
- Progress indicator
- Robust error handling
- Cross-platform support (Windows, Linux, macOS)

## Requirements

- Python 3.9+
- requests

## Installation

```bash
pip install requests
```

## Usage

Download all images from a model page:

```bash
python wikifeetdownloader.py https://www.wikifeet.com/Some_Model
```

Specify a custom output directory:

```bash
python wikifeetdownloader.py https://www.wikifeet.com/Some_Model --download_path ./downloads
```

Use multiple download threads:

```bash
python wikifeetdownloader.py https://www.wikifeet.com/Some_Model --threads 5
```

Configure retries and delay:

```bash
python wikifeetdownloader.py https://www.wikifeet.com/Some_Model --threads 5 --retries 5 --delay 2
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--download_path` | Output directory |
| `--threads` | Number of parallel download threads |
| `--retries` | Retry attempts for failed downloads |
| `--delay` | Delay (in seconds) between retry attempts |

## Disclaimer

This tool downloads images that are already publicly accessible. Users are solely responsible for complying with applicable laws, copyright regulations, and the terms of service of the websites they access.

## Acknowledgements

Thanks to the original project for the initial inspiration.


---

If you find this project useful, feel free to improve it, fork it, or build upon it.

Happy coding! 🍻
