"""
Integration tests for the Webscraper for Indiamart Data Analysis.
"""

import unittest
import os
import shutil

from src.scraper.indiamart_scraper import IndiamartScraper
from src.scraper.data_storage import DataStorage
from src.analyzer.data_cleaner import DataCleaner
from src.analyzer.data_analyzer import DataAnalyzer
from src.models.product import Product


class TestIntegration(unittest.TestCase):
    """Test cases for the integration of scraper, storage, cleaner, and analyzer."""

    def setUp(self):
        """Set up the test fixtures."""
        self.scraper = IndiamartScraper()
        self.storage = DataStorage(output_dir="test_data")
        self.cleaner = DataCleaner()
        self.analyzer = DataAnalyzer()

    def tearDown(self):
        """Clean up the test fixtures."""
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")

    def test_integration_workflow(self):
        """Test the full workflow from scraping to analysis."""
        # Mock the scraping process
        products = [
            Product(name="Product 1", price=100.0, description="Description 1", seller_info="Seller 1"),
            Product(name="Product 2", price=200.0, description="Description 2", seller_info="Seller 2"),
            Product(name="Product 3", price=300.0, description="Description 3", seller_info="Seller 1")
        ]

        # Create a mock ScrapedData object
        from src.models.scraped_data import ScrapedData
        scraped_data = ScrapedData(
            url="http://example.com",
            products=products,
            metadata={"status_code": 200, "content_type": "text/html"}
        )

        # Test storage
        csv_path = self.storage.save_to_csv(scraped_data)
        self.assertTrue(os.path.exists(csv_path))

        # Test cleaning
        cleaned_products = self.cleaner.clean_products(products)
        self.assertEqual(len(cleaned_products), 3)

        # Test conversion to DataFrame
        df = self.cleaner.to_dataframe(cleaned_products)
        self.assertEqual(len(df), 3)

        # Test analysis
        analyzed_data = self.analyzer.analyze(df)
        self.assertIn('average_price', analyzed_data.trends)
        self.assertIn('top_seller', analyzed_data.patterns)
        self.assertIn('price_mean', analyzed_data.statistics)


if __name__ == '__main__':
    unittest.main()