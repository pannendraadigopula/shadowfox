

import requests
from bs4 import BeautifulSoup
import csv
import time
BASE_URL   = "https://books.toscrape.com/catalogue/"
START_URL  = "https://books.toscrape.com/catalogue/page-1.html"
OUTPUT_CSV = "books_toscrape.csv"
MAX_PAGES  = 50        # set to a lower number to scrape fewer pages
DELAY_SEC  = 0.5       # polite delay between requests

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BookScraper/1.0; +https://example.com)"
}

def scrape_books(start_url: str, max_pages: int) -> list[dict]:
    books = []
    url   = start_url
    page  = 1

    while url and page <= max_pages:
        print(f"  Page {page:>2} → {url}")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  ERROR on page {page}: {e}")
            break

        soup = BeautifulSoup(resp.text, "lxml")

        for article in soup.select("article.product_pod"):
            title   = article.h3.a["title"]
            raw_price = article.select_one("p.price_color").text.strip()
            price   = raw_price.encode("ascii", "ignore").decode()   
            rating  = RATING_MAP.get(article.p["class"][1], 0)
            avail   = article.select_one("p.availability").text.strip()
            rel_link = article.h3.a["href"].replace("../", "")
            link    = BASE_URL + rel_link

            books.append({
                "Title":             title,
                "Price (£)":         price,
                "Rating (out of 5)": rating,
                "Availability":      avail,
                "URL":               link,
            })

      
        next_btn = soup.select_one("li.next a")
        url = BASE_URL + next_btn["href"] if next_btn else None
        page += 1
        time.sleep(DELAY_SEC)

    return books


def save_csv(books: list[dict], path: str) -> None:
    fieldnames = ["Title", "Price (£)", "Rating (out of 5)", "Availability", "URL"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
    print(f"\n✓ Saved {len(books)} books to '{path}'")




if __name__ == "__main__":
    print(f"Scraping books.toscrape.com (up to {MAX_PAGES} pages)...\n")
    books = scrape_books(START_URL, MAX_PAGES)
    save_csv(books, OUTPUT_CSV)
