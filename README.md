# Wikifeet Image Downloader

A lightweight Python utility for downloading all publicly available images from supported Wikifeet and WikifeetX model pages.

This project was inspired by an existing downloader but has evolved into its own implementation with numerous improvements and additional features.

Some of these improvements were shared with the original maintainer, who responded positively and intended to integrate them in the future. Since the original project has not seen further development for quite some time, this standalone version was created so the work can continue instead of remaining unused.

## Features

- Download all available images from a model page
- Automatic resume support by skipping existing files
- Parallel downloads
- Configurable retry logic
- Connection timeouts
- Robust error handling
- Progress indicator
- Cross-platform support (Windows, Linux, macOS)

## Requirements

- Python 3.9+
- requests

Install dependencies:

```bash
pip install requests
```

## Usage

Download all images from a model page:

```bash
python downloader.py https://www.wikifeet.com/Some_Model
```

Specify a custom output directory:

```bash
python downloader.py https://www.wikifeet.com/Some_Model --download_path ./downloads
```

Use multiple download threads:

```bash
python downloader.py https://www.wikifeet.com/Some_Model --threads 5
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--download_path` | Output directory |
| `--threads` | Number of parallel downloads |
| `--retries` | Retry count for failed downloads |
| `--delay` | Delay between retry attempts |

## Disclaimer

This tool is intended to download content that is already publicly accessible. Users are responsible for complying with all applicable laws, copyright regulations, and the terms of service of the websites they access.

## Acknowledgements

Thanks to the original project for the initial inspiration.



---

If this project makes your life a little easier, that's great.

Feel free to improve it, fork it, or build upon it.

Happy coding! 🍻
