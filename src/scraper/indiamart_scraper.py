"""
Indiamart Scraper for the Webscraper for Indiamart Data Analysis.

This module provides functionality to scrape product data from Indiamart
using direct JSON extraction method (no Selenium required).
"""

import requests
import json
import re
import os
import time
import random
import csv
from bs4 import BeautifulSoup
from typing import List, Optional

from src.models.product import Product
from src.models.scraped_data import ScrapedData

class IndiamartScraper:
    """Scrapes product data from Indiamart using direct JSON extraction."""

    def __init__(self):
        """Initialize the IndiamartScraper with anti-scraping measures."""
        pass

    def _get_random_delay(self) -> float:
        """Get a random delay between requests to avoid rate limiting."""
        return random.uniform(1.0, 3.0)

    def scrape(self, url: str, max_retries: int = 3) -> ScrapedData:
        """Scrape product data from the given URL using direct JSON extraction.

        Args:
            url: URL of the Indiamart page to scrape.
            max_retries: Maximum number of retry attempts for failed requests.

        Returns:
            ScrapedData: An instance containing the scraped data.

        Raises:
            ValueError: If the URL is invalid or scraping fails after retries.
        """
        if not url:
            raise ValueError("URL cannot be empty")

        if not (url.startswith("https://www.indiamart.com/") or url.startswith("https://dir.indiamart.com/")):
            raise ValueError("URL must start with 'https://www.indiamart.com/' or 'https://dir.indiamart.com/'")

        time.sleep(self._get_random_delay())

        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    delay = self._get_random_delay() * (attempt + 1)
                    time.sleep(delay)

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }

                response = requests.get(url, headers=headers)

                if response.status_code == 403:
                    if attempt < max_retries - 1:
                        continue
                    else:
                        raise ValueError(f"Access forbidden (403) after {max_retries} attempts. Website may have anti-scraping protection.")

                elif response.status_code == 429:
                    retry_after = response.headers.get('Retry-After', 10)
                    if attempt < max_retries - 1:
                        time.sleep(float(retry_after))
                        continue
                    else:
                        raise ValueError(f"Rate limited (429) after {max_retries} attempts.")

                response.raise_for_status()

                if "access denied" in response.text.lower() or "bot detected" in response.text.lower():
                    if attempt < max_retries - 1:
                        continue
                    else:
                        raise ValueError("Anti-bot detection triggered after multiple attempts.")

                break

            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise ValueError(f"Failed to fetch URL after {max_retries} attempts: {e}")
                time.sleep(self._get_random_delay() * (attempt + 2))

        products = self._parse_json_data(response.text)

        csv_path = self.save_to_csv(products)

        debug_html_path = os.path.join("data", "debug", "page_content.html")
        os.makedirs(os.path.dirname(debug_html_path), exist_ok=True)
        with open(debug_html_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

        metadata = {
            "url": url,
            "status_code": response.status_code,
            "content_type": response.headers.get('content-type', 'unknown'),
            "attempts": attempt + 1,
            "debug_html_path": debug_html_path,
            "parsing_method": "json",
            "csv_path": csv_path
        }

        return ScrapedData(url=url, products=products, metadata=metadata)

    def _parse_json_data(self, page_source: str) -> List[Product]:
        """Parse product data from JSON embedded in the page source.

        Args:
            page_source: The raw HTML page source.

        Returns:
            List[Product]: A list of Product instances extracted from JSON data.
        """
        products = []

        try:
            soup = BeautifulSoup(page_source, 'html.parser')
            script = soup.find('script', string=re.compile('window.__INITIAL_STATE__'))
            # print(script)

            if script:
                json_match = re.search(r'window.__INITIAL_STATE__ = (.*?);', script.string, re.DOTALL)
                if json_match:
                    json_data = json_match.group(1)
                    data = json.loads(json_data)
                    # print("data : ",data)

                    if 'data' in data and isinstance(data['data'], list):
                        for product_data in data['data']:
                            try:
                                product_name = product_data.get('p_nm', 'N/A')
                                supplier_name = product_data.get('CMP', 'N/A')
                                price = product_data.get('pr', 'N/A')
                                city = product_data.get('city', 'N/A')
                                address = product_data.get('ad', 'N/A')
                                location = f"{city}, {address}" if city != 'N/A' or address != 'N/A' else "N/A"
                                product_url = product_data.get('p_url', 'N/A')
                                supplier_url = product_data.get('s_url', 'N/A')
                                rating = product_data.get('wt_avg', 'N/A')
                                reviews = product_data.get('tr_c', 'N/A')

                                # Clean price
                                if isinstance(price, str):
                                    price = float(re.sub(r'[^\d.]', '', price)) if re.search(r'\d', price) else 0.0
                                elif not isinstance(price, (int, float)):
                                    price = 0.0

                                description = (
                                    f"Supplier: {supplier_name}\n"
                                    f"Location: {location}\n"
                                    f"Rating: {rating} ({reviews} reviews)\n"
                                    f"Product URL: {product_url}\n"
                                    f"Supplier URL: {supplier_url}"
                                )

                                product = Product(
                                    name=product_name,
                                    price=price,
                                    description=description,
                                    seller_info=supplier_name
                                )
                                products.append(product)

                            except Exception:
                                continue

        except Exception:
            pass

        return products

    def save_to_csv(self, products: List[Product], filename: str = "scraped_data.csv") -> str:
        """Save the scraped products to a CSV file.

        Args:
            products: List of Product instances to save.
            filename: Name of the CSV file to save to.

        Returns:
            str: Path to the saved CSV file.
        """
        os.makedirs("data/raw", exist_ok=True)
        filepath = os.path.join("data/raw", filename)

        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Description', 'Seller Info'])
            for product in products:
                writer.writerow([product.name, product.price, product.description.replace('\n', ' '), product.seller_info])

        return filepath
