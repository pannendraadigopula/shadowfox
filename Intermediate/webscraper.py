import requests
from bs4 import BeautifulSoup
import csv
def scrape_shadowfox():
    url = "https://shadowfox.in"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # Error handling for bad response
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract data
        title = soup.title.text.strip() if soup.title else "No Title"
        headings = [tag.text.strip() for tag in soup.find_all(["h1", "h2"])]

        print("Website Title:", title)
        print("\nHeadings:")
        for h in headings:
            print("-", h)

        # Save to CSV
        with open("shadowfox_data.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(["Title"])
            writer.writerow([title])

            writer.writerow([])
            writer.writerow(["Headings"])

            for h in headings:
                writer.writerow([h])

        print("\n Data saved to shadowfox_data.csv")

    except requests.exceptions.RequestException as e:
        print(" Network Error:", e)

    except Exception as e:
        print(" Unexpected Error:", e)


scrape_shadowfox()
