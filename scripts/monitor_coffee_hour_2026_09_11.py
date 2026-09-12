#!/usr/bin/env python3
"""Emit deterministic availability for the 2026-09-11 Guild Coffee Hour."""
import json
import re
import sys

import browser_cookie3
import requests
from bs4 import BeautifulSoup

URL = "https://www.skool.com/ai-builders-guild-9932/classroom/50af6e4d?md=3ad20c356b7e4e09a39e09da526d991a"
COOKIE_FILE = "/home/tom/.config/google-chrome/Default/Cookies"
TARGET_TITLES = {"september 11", "september 11th"}


def normalized_title(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def main():
    try:
        jar = browser_cookie3.chrome(domain_name=".skool.com", cookie_file=COOKIE_FILE)
        response = requests.get(
            URL,
            cookies=jar,
            timeout=45,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        if "/classroom/" not in response.url:
            raise RuntimeError("authenticated classroom request redirected")
        soup = BeautifulSoup(response.text, "html.parser")
        node = soup.find("script", id="__NEXT_DATA__")
        if not node or not node.string:
            raise RuntimeError("Skool __NEXT_DATA__ was missing")
        data = json.loads(node.string)
        course = data["props"]["pageProps"]["course"]
        matches = []
        for session_set in course.get("children", []):
            set_title = session_set.get("course", {}).get("metadata", {}).get("title", "")
            if set_title != "Coffee Hour":
                continue
            for module in session_set.get("children", []):
                metadata = module.get("course", {}).get("metadata", {})
                if metadata.get("title") != "September 2026":
                    continue
                raw = metadata.get("resources", "[]")
                resources = json.loads(raw) if isinstance(raw, str) else raw
                for resource in resources or []:
                    title = normalized_title(resource.get("title"))
                    filename = normalized_title(resource.get("file_name"))
                    if title in TARGET_TITLES or "9 11 26" in title or "9 11 26" in filename:
                        matches.append({
                            key: resource[key]
                            for key in ("title", "link", "file_id", "file_name", "file_content_type")
                            if resource.get(key)
                        })
        status = "available" if matches else "absent"
        print(json.dumps({"status": status, "date": "2026-09-11", "resources": matches}, sort_keys=True))
    except Exception as exc:
        print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}"}, sort_keys=True))
        sys.exit(1)


if __name__ == "__main__":
    main()
