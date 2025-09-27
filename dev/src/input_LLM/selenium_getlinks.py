#!/usr/bin/env python3
"""
scrape_articles_to_csv.py
---------------------------------
Scrapes every <article> element on a given web page and writes one CSV row per
article with the columns:

    name, status, link, time

• name   – the anchor text inside the article’s <h3> → <a> tag  
• status – text inside the article (first <dd> with a “status” class) or the
           data-disaster-status attribute (if present)  
• link   – absolute URL from the <a> tag inside the article  
• time   – contents of the first <time> tag or empty string if not present

Usage
    python scrape_articles_to_csv.py <url> [output.csv]

Requirements
    pip install selenium webdriver-manager beautifulsoup4

Chrome/Chromium must be installed. The script auto-downloads the correct
chromedriver via webdriver-manager and runs in headless mode.
"""

import sys, csv, time as t
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def init_browser() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless=new")   # Chrome >= 109
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--user-agent=Mozilla/5.0")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                            options=opts)


def parse_article(tag, base_url):
    """Extract (name, status, link, time) tuple from one <article> BeautifulSoup tag."""
    # Name & link
    h3 = tag.find("h3")
    a_tag = h3.find("a") if h3 else None
    name = a_tag.get_text(strip=True) if a_tag else ""
    link = urljoin(base_url, a_tag["href"]) if a_tag and a_tag.get("href") else ""

    # Status: look for <dd class*='status'>, else data-attribute
    status_dd = tag.find("dd", class_=lambda c: c and "status" in c)
    status = status_dd.get_text(strip=True) if status_dd else tag.get("data-disaster-status", "")

    # Time: first <time> element’s text or datetime attr
    time_tag = tag.find("time")
    if time_tag:
        time_val = time_tag.get("datetime", "").strip() or time_tag.get_text(strip=True)
    else:
        time_val = ""

    return name, status, link, time_val


def scrape(url: str):
    """Return list of dictionaries with article data."""
    browser = init_browser()
    try:
        browser.get(url)
        t.sleep(8)  # simple wait; adjust or replace with WebDriverWait if needed
        soup = BeautifulSoup(browser.page_source, "html.parser")
    finally:
        browser.quit()

    articles = soup.find_all("article")
    rows = [parse_article(a, url) for a in articles]
    return rows


def save_csv(rows, outfile):
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "status", "link", "time"])
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows → {outfile}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_articles_to_csv.py <url> [output.csv]")
        sys.exit(1)

    target_url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "articles.csv"

    data_rows = scrape(target_url)
    if data_rows:
        save_csv(data_rows, output_file)
    else:
        print("No <article> elements found – nothing written.")
