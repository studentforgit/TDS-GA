import json
import httpx
from datetime import datetime, timezone
from lxml import html
from typing import List, Dict

def scrape_imdb() -> List[Dict[str, str]]:
    """Scrape IMDb Top 250 movies using httpx and lxml."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; IMDbBot/1.0)"}
    response = httpx.get("https://www.imdb.com/chart/top/", headers=headers)
    response.raise_for_status()

    tree = html.fromstring(response.text)
    movies = []

    for item in tree.xpath('//li[contains(@class, "ipc-metadata-list-summary-item")]'):
        title = item.xpath('.//h3[contains(@class, "ipc-title__text")]/text()')
        year = item.xpath('.//span[contains(@class, "cli-title-metadata-item")]/text()')
        rating = item.xpath('.//span[contains(@class, "ipc-rating-star")]/text()')

        if title and year and rating:
            movies.append({
                "title": title[0].strip(),
                "year": year[0].strip(),
                "rating": rating[0].strip(),
            })

    return movies

# Scrape data and save with timestamp
now = datetime.now(timezone.utc)
filename = f'imdb-top250-{now.strftime("%Y-%m-%d")}.json'

with open(filename, "w", encoding="utf-8") as f:
    json.dump({"timestamp": now.isoformat(), "movies": scrape_imdb()}, f, indent=4)

print(f"Scraped data saved to {filename}")
