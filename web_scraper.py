
import requests
from bs4 import BeautifulSoup
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "quotes.json")
TXT_FILE = os.path.join(BASE_DIR, "quotes.txt")

BASE_URL = "https://quotes.toscrape.com/"


def scrape_quotes():
    url = BASE_URL
    quotes_data = []

    try:
        while url:
            print("Scraping:", url)

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            quote_elements = soup.find_all("div", class_="quote")

            for quote in quote_elements:
                text_element = quote.find("span", class_="text")
                author_element = quote.find("small", class_="author")

                if text_element and author_element:
                    quotes_data.append({
                        "quote": text_element.get_text(strip=True),
                        "author": author_element.get_text(strip=True)
                    })

            next_page = soup.find("li", class_="next")

            if next_page and next_page.find("a"):
                next_link = next_page.find("a")["href"]
                url = requests.compat.urljoin(url, next_link)
            else:
                url = None

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(
                quotes_data, file,
                indent=4, ensure_ascii=False
            )

        with open(TXT_FILE, "w", encoding="utf-8") as file:
            for number, item in enumerate(quotes_data, start=1):
                file.write(f"{number}. {item['quote']}\n")
                file.write(f"Author: {item['author']}\n\n")

        print(f"\nSuccessfully saved {len(quotes_data)} quotes!")

    except requests.exceptions.RequestException as error:
        print("Website connection failed:", error)


def load_quotes():
    if not os.path.exists(JSON_FILE):
        print("No saved quotes. Please scrape the website first.")
        return []

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid JSON data.")
            return []

        return data

    except (OSError, json.JSONDecodeError) as error:
        print("Could not read saved quotes:", error)
        return []


def view_quotes():
    quotes = load_quotes()

    if not quotes:
        print("No quotes available.")
        return

    print("\n===== SAVED QUOTES =====")

    for number, item in enumerate(quotes, start=1):
        print(f"\n{number}. {item['quote']}")
        print(f"Author: {item['author']}")


def search_author():
    quotes = load_quotes()

    if not quotes:
        print("No quotes available. Scrape the website first.")
        return

    author_name = input("Enter author name: ").strip().casefold()

    if not author_name:
        print("Please enter an author name.")
        return

    found = False

    for item in quotes:
        if author_name in item["author"].casefold():
            print(f"\nQuote: {item['quote']}")
            print(f"Author: {item['author']}")
            found = True

    if not found:
        print("No quotes found for that author.")


def main():
    while True:
        print("\n===== WEB SCRAPER MENU =====")
        print("1. Scrape quotes from website")
        print("2. View saved quotes")
        print("3. Search quotes by author")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            scrape_quotes()
        elif choice == "2":
            view_quotes()
        elif choice == "3":
            search_author()
        elif choice == "4":
            print("Thank you for using Web Scraper!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
