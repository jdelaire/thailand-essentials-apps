#!/usr/bin/env python3
import os
import re
import sys
import json
import time
from typing import List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


MARKDOWN_FILES = [
    "food.md",
    "transport.md",
    "shopping.md",
    "social.md",
    "money.md",
    "housing.md",
]

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
SCREENSHOTS_DIR = os.path.abspath(SCREENSHOTS_DIR)


APP_STORE_LINK_WITH_CC_RE = re.compile(
    r"https?://apps\.apple\.com/(?:(?P<cc>[a-z]{2})/app|app)/[^/]+/id(?P<id>\d+)",
    re.IGNORECASE,
)

IMG_SRC_RE = re.compile(r"<img\s+src=\"screenshots/([^\"]+)\"", re.IGNORECASE)


def parse_markdown_for_apps(md_path: str) -> List[Tuple[str, str, List[str]]]:
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    groups: List[Tuple[str, str, List[str]]] = []
    # group local screenshot filenames following each Download section
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "**Download:**" in line and "apps.apple.com" in line:
            m_link = APP_STORE_LINK_WITH_CC_RE.search(line)
            app_id = None
            country_code = "us"
            if m_link:
                app_id = m_link.group("id")
                if m_link.group("cc"):
                    country_code = m_link.group("cc").lower()
            # collect following <img ...> lines until blank or next section
            j = i + 1
            local_imgs: List[str] = []
            # search forward for a block of <img ...> tags inside a div
            # limit to next 20 lines to avoid spanning too far
            limit = min(len(lines), i + 25)
            while j < limit:
                m = IMG_SRC_RE.search(lines[j])
                if m:
                    local_imgs.append(m.group(1))
                elif local_imgs and ("</div>" in lines[j] or lines[j].strip() == ""):
                    break
                j += 1
            if local_imgs and app_id:
                groups.append((app_id, country_code, local_imgs[:3]))
        i += 1

    return groups


def lookup_app_screenshots(app_id: str, country_code: str) -> List[str]:
    def _query(cc: Optional[str]) -> List[str]:
        url = f"https://itunes.apple.com/lookup?id={app_id}&entity=software"
        if cc:
            url += f"&country={cc}"
        req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        })
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        results = data.get("results", [])
        if not results:
            return []
        screenshot_urls: List[str] = []
        primary = results[0]
        for key in ("screenshotUrls", "ipadScreenshotUrls"):
            urls = primary.get(key, [])
            for u in urls:
                if u not in screenshot_urls:
                    screenshot_urls.append(u)
                if len(screenshot_urls) >= 3:
                    break
            if len(screenshot_urls) >= 3:
                break
        return screenshot_urls

    # Try specified country, then a broader fallback list
    fallback_countries: List[Optional[str]] = [
        country_code or None,
        "th",
        "us",
        "gb",
        "sg",
        "id",
        "vn",
        "my",
        "ph",
        None,
    ]
    seen: set = set()
    for cc in fallback_countries:
        if cc in seen:
            continue
        seen.add(cc)
        try:
            urls = _query(cc if cc else None)
        except Exception:
            urls = []
        if urls:
            return urls
    return []


def download_bytes(url: str) -> Optional[bytes]:
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        })
        with urlopen(req, timeout=30) as resp:
            return resp.read()
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def save_bytes(content: bytes, dest_path: str) -> None:
    ensure_dir(dest_path)
    with open(dest_path, "wb") as f:
        f.write(content)


def main() -> int:
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    found: List[Tuple[str, str, List[str]]] = []

    for md in MARKDOWN_FILES:
        md_path = os.path.join(workspace_root, md)
        if not os.path.exists(md_path):
            continue
        groups = parse_markdown_for_apps(md_path)
        if groups:
            found.extend(groups)

    if not found:
        print("No apps with App Store links found in markdown files.")
        return 1

    print(f"Found {len(found)} app sections with screenshots to update.")

    updated_count = 0

    for app_id, country_code, local_files in found:
        try:
            urls = lookup_app_screenshots(app_id, country_code)
        except Exception as e:
            print(f"Lookup failed for {app_id}: {e}")
            urls = []

        if not urls:
            print(f"No screenshots for {app_id}")
            continue

        for idx, local_name in enumerate(local_files):
            if idx >= len(urls):
                break
            src_url = urls[idx]
            content = download_bytes(src_url)
            if content is None:
                continue
            dest_path = os.path.join(SCREENSHOTS_DIR, local_name)
            try:
                save_bytes(content, dest_path)
                print(f"Wrote {dest_path} from {src_url}")
            except Exception as e:
                print(f"Failed to write {dest_path}: {e}")
        updated_count += 1
        time.sleep(0.4)  # be polite to API

    print(f"Updated {updated_count} apps' screenshots.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

