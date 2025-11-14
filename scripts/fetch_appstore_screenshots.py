#!/usr/bin/env python3
import os
import re
import sys
import json
import time
from typing import List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


# When run without explicit args, the script scans these markdown files
# to discover apps and refresh their screenshots.
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
ICONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))


APP_STORE_LINK_WITH_CC_RE = re.compile(
    r"https?://apps\.apple\.com/(?:(?P<cc>[a-z]{2})/app|app)/[^/]+/id(?P<id>\d+)",
    re.IGNORECASE,
)

# Extract Google Play package name from the same Download line
GOOGLE_PLAY_PKG_RE = re.compile(
    r"https?://play\.google\.com/store/apps/details\?id=(?P<pkg>[A-Za-z0-9_\.]+)",
    re.IGNORECASE,
)

IMG_SRC_RE = re.compile(r"<img\s+src=\"screenshots/([^\"]+)\"", re.IGNORECASE)


def parse_markdown_for_apps(md_path: str) -> List[Tuple[Optional[str], str, Optional[str], List[str]]]:
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    groups: List[Tuple[Optional[str], str, Optional[str], List[str]]] = []
    # group local screenshot filenames following each Download section
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "**Download:**" in line and ("apps.apple.com" in line or "play.google.com" in line):
            m_link = APP_STORE_LINK_WITH_CC_RE.search(line)
            m_play = GOOGLE_PLAY_PKG_RE.search(line)
            app_id: Optional[str] = None
            play_pkg: Optional[str] = None
            country_code = "us"
            if m_link:
                app_id = m_link.group("id")
                if m_link.group("cc"):
                    country_code = m_link.group("cc").lower()
            if m_play:
                play_pkg = m_play.group("pkg")
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
            if local_imgs and (app_id or play_pkg):
                groups.append((app_id, country_code, play_pkg, local_imgs[:3]))
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


def lookup_app_icon_url(app_id: str, country_code: Optional[str] = None) -> Optional[str]:
    """Return the best App Store artwork URL for the app (prefer 512px)."""
    url = f"https://itunes.apple.com/lookup?id={app_id}&entity=software"
    if country_code:
        url += f"&country={country_code}"
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        })
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        results = data.get("results", [])
        if not results:
            return None
        primary = results[0]
        # Prefer larger artwork if present
        for key in ("artworkUrl512", "artworkUrl100", "artworkUrl60"):
            u = primary.get(key)
            if u:
                return u
    except Exception:
        return None
    return None


def _decode_play_html(raw: str) -> str:
    # Normalize common escaped sequences that appear in inline JSON blobs
    txt = raw.replace("\\u003d", "=").replace("\\u0026", "&")
    txt = txt.replace("\u003d", "=").replace("\u0026", "&")
    txt = txt.replace("&amp;", "&")
    return txt


def lookup_play_screenshots(package_name: str) -> List[str]:
    if not package_name:
        return []
    url = (
        f"https://play.google.com/store/apps/details?id={package_name}&hl=en_US&gl=US&pli=1"
    )
    try:
        req = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        with urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Failed to load Play page for {package_name}: {e}")
        return []

    html = _decode_play_html(html)

    # Try targeted attribute first
    urls: List[str] = []
    seen: set = set()

    # 1) Legacy attribute sometimes present
    m1 = re.findall(r'data-screenshot-url=\"(https://play-lh\.googleusercontent\.com/[^\"]+)\"', html)
    for u in m1:
        if u not in seen:
            urls.append(u)
            seen.add(u)

    # 2) Generic: grab all lh googleusercontent candidates in the page
    m2 = re.findall(r"https://play-lh\.googleusercontent\.com/[A-Za-z0-9_\-~\./=]+", html)
    for u in m2:
        if u not in seen:
            urls.append(u)
            seen.add(u)

    def normalize_play_url(u: str) -> str:
        if "play-lh.googleusercontent.com" not in u:
            return u
        # Strip any existing sizing directive and force a decent portrait size
        base = u.split("=")[0]
        return base + "=w720-h1440-rw"

    # Normalize to high-res portrait variants
    urls = [normalize_play_url(u) for u in urls]

    # Heuristics: prefer portrait screenshots (height >= width) and discard tiny/icon/feature graphics
    filtered: List[str] = []
    for u in urls:
        # Find size hints like =w720-h1544 or =h1544-w720 or -w720-h1544 on the tail
        dims = re.search(r"[=\-]w(\d+)-h(\d+)", u)
        if not dims:
            dims = re.search(r"[=\-]h(\d+)-w(\d+)", u)
            if dims:
                height = int(dims.group(1))
                width = int(dims.group(2))
            else:
                # No size hint, keep as fallback at end
                filtered.append(u)
                continue
        else:
            width = int(dims.group(1))
            height = int(dims.group(2))

        # Discard obvious feature graphics (very wide) and icons (small or square-ish)
        if width < 250 or height < 400:
            continue
        if height < width:
            # likely landscape banner
            continue
        filtered.append(u)

    # Keep order, unique, top 3
    out: List[str] = []
    seen2: set = set()
    for u in filtered:
        if u not in seen2:
            out.append(u)
            seen2.add(u)
        if len(out) >= 3:
            break
    return out


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


def is_valid_image_bytes(buf: bytes) -> bool:
    if not buf or len(buf) < 1024:
        return False
    # JPEG
    if buf.startswith(b"\xff\xd8\xff"):
        return True
    # PNG
    if buf.startswith(b"\x89PNG\r\n\x1a\n"):
        return True
    # WebP (RIFF....WEBP)
    if len(buf) >= 12 and buf[0:4] == b"RIFF" and buf[8:12] == b"WEBP":
        return True
    return False


def is_local_image_valid(path: str) -> bool:
    try:
        st = os.stat(path)
        if st.st_size < 2048:
            return False
        with open(path, "rb") as f:
            head = f.read(16)
        # Basic magic check
        if head.startswith(b"\xff\xd8\xff"):
            return True
        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            return True
        if head[0:4] == b"RIFF":
            return True
        return False
    except FileNotFoundError:
        return False
    except Exception:
        return False


def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def save_bytes(content: bytes, dest_path: str) -> None:
    ensure_dir(dest_path)
    with open(dest_path, "wb") as f:
        f.write(content)


def try_save_resized_jpg(content: bytes, dest_path: str, target_w: int, target_h: int) -> bool:
    """Attempt to convert and resize image bytes to a JPG at target size.
    Returns True on success. Falls back to raw save by caller on failure.
    """
    try:
        from io import BytesIO
        from PIL import Image
        im = Image.open(BytesIO(content)).convert("RGB")
        # Fit inside target while preserving orientation; then pad/crop to exact
        im = im.copy()
        im.thumbnail((target_w, target_h), Image.LANCZOS)
        # Create exact-size canvas and center the thumbnail
        canvas = Image.new("RGB", (target_w, target_h), (255, 255, 255))
        x = (target_w - im.width) // 2
        y = (target_h - im.height) // 2
        canvas.paste(im, (x, y))
        ensure_dir(dest_path)
        canvas.save(dest_path, format="JPEG", quality=88, optimize=True)
        return True
    except Exception:
        return False


def try_save_resized_png(content: bytes, dest_path: str, size: int = 64) -> bool:
    """Attempt to convert and resize image bytes to a square PNG of given size."""
    try:
        from io import BytesIO
        from PIL import Image
        im = Image.open(BytesIO(content))
        # Convert to RGBA to keep transparency if any
        im = im.convert("RGBA")
        # Fit into square
        im.thumbnail((size, size), Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        x = (size - im.width) // 2
        y = (size - im.height) // 2
        canvas.paste(im, (x, y))
        ensure_dir(dest_path)
        canvas.save(dest_path, format="PNG", optimize=True)
        return True
    except Exception:
        return False


def refresh_from_markdown() -> int:
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    found: List[Tuple[Optional[str], str, Optional[str], List[str]]] = []

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
    force_refresh = os.environ.get("FORCE_REFRESH", "0").strip() in ("1", "true", "True")

    for app_id, country_code, play_pkg, local_files in found:
        try:
            urls = lookup_app_screenshots(app_id, country_code) if app_id else []
        except Exception as e:
            print(f"Lookup failed for App Store id {app_id}: {e}")
            urls = []

        if not urls:
            # Try Google Play fallback
            if play_pkg:
                try:
                    urls = lookup_play_screenshots(play_pkg)
                except Exception as e:
                    print(f"Play lookup failed for {play_pkg}: {e}")
                    urls = []
            if not urls:
                print(f"No screenshots found for app (itunes {app_id}) (play {play_pkg})")
                continue

        # If we have fewer than needed from Apple, try to top up with Play
        if app_id and play_pkg and len(urls) < len(local_files):
            try:
                play_urls = lookup_play_screenshots(play_pkg)
            except Exception as e:
                print(f"Play lookup failed for {play_pkg}: {e}")
                play_urls = []
            for u in play_urls:
                if u not in urls:
                    urls.append(u)
                if len(urls) >= len(local_files):
                    break

        wrote_any = False
        for idx, local_name in enumerate(local_files):
            dest_path = os.path.join(SCREENSHOTS_DIR, local_name)
            needs_update = force_refresh or not is_local_image_valid(dest_path)
            if idx >= len(urls):
                if needs_update:
                    print(f"Missing source for {dest_path} and not enough URLs fetched.")
                continue
            if not needs_update:
                # Skip existing valid file
                continue
            src_url = urls[idx]
            content = download_bytes(src_url)
            if content is None:
                continue
            if not is_valid_image_bytes(content):
                print(f"Downloaded invalid image bytes for {dest_path} from {src_url}")
                continue
            try:
                save_bytes(content, dest_path)
                wrote_any = True
                print(f"Wrote {dest_path} from {src_url}")
            except Exception as e:
                print(f"Failed to write {dest_path}: {e}")
        if wrote_any:
            updated_count += 1
        time.sleep(0.4)  # be polite to API

    print(f"Updated {updated_count} apps' screenshots.")
    return 0


def fetch_single_app(app_id: str, base_name: str, country_code: Optional[str] = None,
                     count: int = 3, fetch_icon: bool = True,
                     play_package: Optional[str] = None) -> int:
    """Fetch screenshots (and icon) for a single App Store app.
    Saves screenshots as screenshots/{base_name}-1.jpg .. -{count}.jpg
    Saves icon as icons/{base_name}.png
    """
    try:
        urls = lookup_app_screenshots(app_id, (country_code or "us"))
    except Exception as e:
        print(f"Lookup failed for App Store id {app_id}: {e}")
        urls = []

    if not urls and play_package:
        try:
            urls = lookup_play_screenshots(play_package)
        except Exception as e:
            print(f"Play lookup failed for {play_package}: {e}")
            urls = []
        if not urls:
            print(f"No screenshots found for app id {app_id} or Play package {play_package}.")
        else:
            print(f"Using Google Play screenshots as fallback for {play_package}.")
    if not urls:
        print(f"No screenshots found for app id {app_id}.")
    else:
        # limit to desired count
        urls = urls[:max(1, count)]
        for idx, src_url in enumerate(urls, start=1):
            dest_name = f"{base_name}-{idx}.jpg"
            dest_path = os.path.join(SCREENSHOTS_DIR, dest_name)
            content = download_bytes(src_url)
            if content is None:
                continue
            # Prefer resized JPG for consistency with site assets
            if not try_save_resized_jpg(content, dest_path, 392, 696):
                # Fallback: save original bytes
                save_bytes(content, dest_path)
            print(f"Saved screenshot {dest_path} from {src_url}")

    if fetch_icon:
        icon_url = lookup_app_icon_url(app_id, country_code)
        if icon_url:
            icon_bytes = download_bytes(icon_url)
            if icon_bytes:
                icon_dest = os.path.join(ICONS_DIR, f"{base_name}.png")
                if not try_save_resized_png(icon_bytes, icon_dest, 64):
                    save_bytes(icon_bytes, icon_dest)
                print(f"Saved icon {icon_dest} from {icon_url}")
        else:
            print(f"No icon URL found for app id {app_id}.")

    return 0


def main() -> int:
    # Simple CLI: optional args for direct fetch
    # Usage examples:
    #   python scripts/fetch_appstore_screenshots.py --id 123456 --name myapp --country th --count 3 --no-icon
    args = sys.argv[1:]
    if args and ("--id" in args or "--name" in args):
        def _get_flag(flag: str, default: Optional[str] = None) -> Optional[str]:
            if flag in args:
                i = args.index(flag)
                if i + 1 < len(args):
                    return args[i + 1]
            return default
        app_id = _get_flag("--id")
        base_name = _get_flag("--name") or (f"app-{app_id}" if app_id else None)
        country = _get_flag("--country")
        count_str = _get_flag("--count", "3") or "3"
        no_icon = "--no-icon" in args
        play_pkg = _get_flag("--play")
        if not app_id or not base_name:
            print("--id and --name are required when using direct mode.")
            return 2
        try:
            count = max(1, int(count_str))
        except ValueError:
            count = 3
        return fetch_single_app(app_id, base_name, country, count, fetch_icon=(not no_icon), play_package=play_pkg)

    # Default behavior: refresh via markdown discovery
    return refresh_from_markdown()


if __name__ == "__main__":
    sys.exit(main())
