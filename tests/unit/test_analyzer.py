"""
Unit tests for the analyzer module.
"""

import unittest
import pandas as pd

from src.analyzer.data_cleaner import DataCleaner
from src.analyzer.data_analyzer import DataAnalyzer
from src.models.product import Product


class TestDataCleaner(unittest.TestCase):
    """Test cases for the DataCleaner class."""

    def setUp(self):
        """Set up the test fixtures."""
        self.cleaner = DataCleaner()

    def test_clean_products(self):
        """Test cleaning of product data."""
        products = [
            Product(name="  Product 1  ", price=100.0, description="  Description 1  ", seller_info="  Seller 1  "),
            Product(name="", price=-10.0, description="", seller_info="")
        ]

        cleaned_products = self.cleaner.clean_products(products)

        self.assertEqual(len(cleaned_products), 2)
        self.assertEqual(cleaned_products[0].name, "Product 1")
        self.assertEqual(cleaned_products[0].price, 100.0)
        self.assertEqual(cleaned_products[0].description, "Description 1")
        self.assertEqual(cleaned_products[0].seller_info, "Seller 1")
        self.assertEqual(cleaned_products[1].name, "Unknown")
        self.assertEqual(cleaned_products[1].price, 0.0)
        self.assertEqual(cleaned_products[1].description, "No description")
        self.assertEqual(cleaned_products[1].seller_info, "Unknown seller")

    def test_to_dataframe(self):
        """Test conversion of products to DataFrame."""
        products = [
            Product(name="Product 1", price=100.0, description="Description 1", seller_info="Seller 1"),
            Product(name="Product 2", price=200.0, description="Description 2", seller_info="Seller 2")
        ]

        df = self.cleaner.to_dataframe(products)

        self.assertEqual(len(df), 2)
        self.assertListEqual(list(df.columns), ['name', 'price', 'description', 'seller_info'])


class TestDataAnalyzer(unittest.TestCase):
    """Test cases for the DataAnalyzer class."""

    def setUp(self):
        """Set up the test fixtures."""
        self.analyzer = DataAnalyzer()

    def test_analyze(self):
        """Test analysis of product data."""
        data = {
            'name': ['Product 1', 'Product 2', 'Product 3'],
            'price': [100.0, 200.0, 300.0],
            'description': ['Description 1', 'Description 2', 'Description 3'],
            'seller_info': ['Seller 1', 'Seller 2', 'Seller 1']
        }
        df = pd.DataFrame(data)

        analyzed_data = self.analyzer.analyze(df)

        self.assertIn('average_price', analyzed_data.trends)
        self.assertIn('top_seller', analyzed_data.patterns)
        self.assertIn('price_mean', analyzed_data.statistics)

    def test_analyze_empty_dataframe(self):
        """Test analysis with an empty DataFrame."""
        df = pd.DataFrame()

        with self.assertRaises(ValueError):
            self.analyzer.analyze(df)


if __name__ == '__main__':
    unittest.main()