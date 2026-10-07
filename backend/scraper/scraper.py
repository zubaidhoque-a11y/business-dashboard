"""
Polite web scraper template for a business directory.

IMPORTANT
- Check the site's robots.txt and Terms of Service before scraping.
  This script refuses to fetch URLs that robots.txt disallows.
- Website HTML differs per site and changes often. The CSS selectors below
  are PLACEHOLDERS: open the page in your browser, right click -> Inspect,
  and update them to match the real page.
- If the site blocks you or needs login/JS-heavy rendering, don't try to
  bypass it. Use mock_data.py and explain this in your README.

Run:  python scraper.py   ->  creates listings_scraped.csv
"""
import csv
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

# ----- CONFIG: edit these -----
SOURCE_NAME = "ExampleDirectory"          # shown in the 'source' column
BASE_URL = "https://www.example-directory.com"
# URL pattern with {category} and {city} placeholders. Fill in from the real site.
SEARCH_URL = BASE_URL + "/{city}/{category}?page={page}"
CITIES = ["Kolkata", "Delhi", "Mumbai"]
CATEGORIES = ["restaurants", "gyms", "salons"]
MAX_PAGES = 3
DELAY_SECONDS = 3                          # be gentle with the server
HEADERS = {"User-Agent": "Mozilla/5.0 (student-assignment scraper; contact: you@example.com)"}

# Placeholder CSS selectors: UPDATE THESE for your chosen site
CARD_SELECTOR = "div.listing-card"
NAME_SELECTOR = "h2.name"
ADDRESS_SELECTOR = "span.address"
PHONE_SELECTOR = "span.phone"
# --------------------------------

robots = RobotFileParser()
robots.set_url(BASE_URL + "/robots.txt")
try:
    robots.read()
except Exception:
    print("Could not read robots.txt: proceed carefully / check manually.")


def allowed(url: str) -> bool:
    return robots.can_fetch(HEADERS["User-Agent"], url)


def text_of(card, selector):
    el = card.select_one(selector)
    return el.get_text(strip=True) if el else ""


def scrape_page(url, city, category):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        print(f"  Skipped ({resp.status_code}): {url}")
        return None  # blocked or no more pages
    soup = BeautifulSoup(resp.text, "html.parser")
    rows = []
    for card in soup.select(CARD_SELECTOR):
        name = text_of(card, NAME_SELECTOR)
        if not name:
            continue
        rows.append({
            "business_name": name,
            "category": category.title(),
            "city": city,
            "address": text_of(card, ADDRESS_SELECTOR),
            "phone": text_of(card, PHONE_SELECTOR),
            "source": SOURCE_NAME,
        })
    return rows


def main():
    all_rows = []
    for city in CITIES:
        for category in CATEGORIES:
            for page in range(1, MAX_PAGES + 1):
                url = SEARCH_URL.format(city=city.lower(), category=category, page=page)
                if not allowed(url):
                    print(f"Disallowed by robots.txt, skipping: {url}")
                    break
                print(f"Scraping {url}")
                rows = scrape_page(url, city, category)
                time.sleep(DELAY_SECONDS)
                if not rows:
                    break
                all_rows.extend(rows)

    if not all_rows:
        print("No rows scraped. Check selectors/URL, or use mock_data.py.")
        return

    with open("listings_scraped.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        w.writeheader()
        w.writerows(all_rows)
    print(f"Saved {len(all_rows)} rows to listings_scraped.csv")


if __name__ == "__main__":
    main()
