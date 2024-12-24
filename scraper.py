import requests
from bs4 import BeautifulSoup
import csv
import logging

class WebScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page_content(self):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            logging.info(f"Successfully fetched content from {self.url}")
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching the page content: {e}")
            return None

    def extract_data(self):
        soup = self.fetch_page_content()
        if not soup:
            return []

        data = []
        for tag in soup.find_all("a", href=True):
            title = tag.text.strip() if tag.text.strip() else "No Title"
            link = tag['href'] if 'href' in tag.attrs else "No Link"
            data.append({"Title": title, "Link": link})
        return data

    def save_to_csv(self, data, filename="output.csv"):
        if not data:
            logging.warning("No data to save.")
            return

        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Title", "Link"])
                writer.writeheader()
                writer.writerows(data)
                logging.info(f"Data successfully saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving data to CSV: {e}")

def main():
    target_url = "http://books.toscrape.com/"  # Replace with the URL of your choice
    scraper = WebScraper(target_url)
    data = scraper.extract_data()
    scraper.save_to_csv(data)

if __name__ == "__main__":
    main()
