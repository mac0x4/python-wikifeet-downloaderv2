import argparse
import json
import logging
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List

import requests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

HEADERS = {"User-Agent": "Mozilla/5.0"}
PAGE_PATTERN = re.compile(r"https://(www\.)?(wikifeet|wikifeetx)\.com/.+")


class PageDataParser:
    DATA_MARKER = "tdata = "

    def __init__(self, html: str = ""):
        self.html = html

    def parse(self) -> Dict:
        start = self.html.find(self.DATA_MARKER)
        if start == -1:
            logging.error("Data block not found.")
            return {}

        start += len(self.DATA_MARKER)
        end = self.html.find("\n", start)

        if end == -1:
            logging.error("Data block end not found.")
            return {}

        raw_data = self.html[start:end].strip().rstrip(";")

        try:
            return json.loads(raw_data)
        except json.JSONDecodeError as exc:
            logging.error(f"Could not parse data block: {exc}")
            return {}


class ImageUrlFactory:
    def __init__(self, page_slug: str):
        self.page_slug = page_slug.replace("_", "-")

    def make_url(self, image_id: int) -> str:
        return f"https://pics.wikifeet.com/{self.page_slug}-Feet-{image_id}.jpg"


class ImageFetcher:
    def __init__(self, output_dir: Path, retries: int = 3, delay: float = 1.0):
        self.output_dir = Path(output_dir)
        self.retries = retries
        self.delay = delay

    def fetch(self, url: str) -> bool:
        filename = url.rsplit("/", 1)[-1]
        target = self.output_dir / filename

        if target.exists():
            logging.debug(f"Skipped existing file: {filename}")
            return False

        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(url, headers=HEADERS, timeout=10)

                if response.status_code == 200:
                    target.write_bytes(response.content)
                    logging.debug(f"Saved: {filename}")
                    return True

                logging.warning(f"HTTP {response.status_code} on attempt {attempt}: {url}")

            except requests.RequestException as exc:
                logging.warning(f"Request failed on attempt {attempt}: {exc}")

            time.sleep(self.delay)

        logging.error(f"Failed after {self.retries} attempts: {url}")
        return False


def extract_image_ids(data: Dict) -> List[int]:
    gallery = data.get("gallery", [])

    image_ids = []
    for item in gallery:
        image_id = item.get("pid")
        if image_id is not None:
            image_ids.append(image_id)

    return sorted(image_ids)


def fetch_page(url: str) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException as exc:
        logging.error(f"Page request failed: {exc}")
        sys.exit(1)

    if response.status_code != 200:
        logging.error(f"Could not fetch page: HTTP {response.status_code}")
        sys.exit(1)

    return response.text


def run() -> None:
    parser = argparse.ArgumentParser(description="Image downloader for supported pages.")
    parser.add_argument("url", help="Page URL")
    parser.add_argument("--download_path", default=None, help="Output directory")
    parser.add_argument("--threads", type=int, default=1, help="Number of parallel downloads")
    parser.add_argument("--retries", type=int, default=3, help="Retry count per image")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between retries")

    args = parser.parse_args()
    url = args.url.strip()

    if not PAGE_PATTERN.match(url):
        logging.error("Unsupported or invalid URL.")
        sys.exit(1)

    page_slug = url.rstrip("/").rsplit("/", 1)[-1]
    logging.info(f"Page: {page_slug}")

    html = fetch_page(url)

    parser = PageDataParser(html)
    data = parser.parse()

    if not data:
        logging.error("No usable page data found.")
        sys.exit(1)

    image_ids = extract_image_ids(data)

    if not image_ids:
        logging.error("No image IDs found.")
        sys.exit(1)

    output_dir = Path(args.download_path) if args.download_path else Path.cwd() / page_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Output directory: {output_dir.resolve()}")

    url_factory = ImageUrlFactory(page_slug)
    fetcher = ImageFetcher(output_dir, retries=args.retries, delay=args.delay)

    image_urls = [url_factory.make_url(image_id) for image_id in image_ids]

    downloaded = 0
    skipped = 0
    total = len(image_urls)

    start_time = time.time()

    try:
        with ThreadPoolExecutor(max_workers=max(1, args.threads)) as executor:
            futures = [executor.submit(fetcher.fetch, image_url) for image_url in image_urls]

            for index, future in enumerate(as_completed(futures), start=1):
                try:
                    if future.result():
                        downloaded += 1
                    else:
                        skipped += 1
                except Exception as exc:
                    logging.error(f"Download task failed: {exc}")

                progress = (index / total) * 100
                print(
                    f"Progress: {progress:.1f}% ({downloaded} new, {skipped} skipped)",
                    end="\r",
                )

    except KeyboardInterrupt:
        logging.warning("Interrupted by user.")
        sys.exit(1)

    elapsed = time.time() - start_time
    logging.info(
        f"\nDone: {downloaded} new, {skipped} skipped, {elapsed:.1f}s elapsed"
    )


if __name__ == "__main__":
    run()
