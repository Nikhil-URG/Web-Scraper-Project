"""
Unit tests for the scraper module.
"""

import unittest
from unittest.mock import patch, MagicMock

from src.scraper.indiamart_scraper import IndiamartScraper
from src.models.product import Product


class TestIndiamartScraper(unittest.TestCase):
    """Test cases for the IndiamartScraper class."""

    def setUp(self):
        """Set up the test fixtures."""
        self.scraper = IndiamartScraper()

    @patch('requests.Session.get')
    def test_scrape_success(self, mock_get):
        """Test successful scraping of product data."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'text/html'}
        mock_response.text = """
        <html>
            <body>
                <div class='product'>
                    <h2>Test Product</h2>
                    <span class='price'>₹100</span>
                    <p class='description'>Test Description</p>
                    <div class='seller'>Test Seller</div>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        # Call the scrape method
        scraped_data = self.scraper.scrape("https://dir.indiamart.com/impcat/pvc-pipes.html")

        # Assertions
        self.assertEqual(len(scraped_data.products), 1)
        self.assertEqual(scraped_data.products[0].name, "Test Product")
        self.assertEqual(scraped_data.products[0].price, 100.0)
        self.assertEqual(scraped_data.products[0].description, "Test Description")
        self.assertEqual(scraped_data.products[0].seller_info, "Test Seller")

    @patch('requests.Session.get')
    def test_scrape_empty_url(self, mock_get):
        """Test scraping with an empty URL."""
        with self.assertRaises(ValueError):
            self.scraper.scrape("")

    @patch('requests.Session.get')
    def test_scrape_failure(self, mock_get):
        """Test scraping with a failed request."""
        mock_get.side_effect = Exception("Request failed")

        with self.assertRaises(ValueError):
            self.scraper.scrape("http://example.com")


if __name__ == '__main__':
    unittest.main()