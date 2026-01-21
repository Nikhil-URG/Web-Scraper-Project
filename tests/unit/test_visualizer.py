"""
Unit tests for the visualizer module.
"""

import unittest
import pandas as pd
import os

from src.visualizer.plot_generator import PlotGenerator


class TestPlotGenerator(unittest.TestCase):
    """Test cases for the PlotGenerator class."""

    def setUp(self):
        """Set up the test fixtures."""
        self.plot_generator = PlotGenerator()
        self.output_dir = "test_output"
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        """Clean up the test fixtures."""
        import shutil
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_generate_price_plot(self):
        """Test generation of price plot."""
        data = {
            'name': ['Product 1', 'Product 2', 'Product 3'],
            'price': [100.0, 200.0, 300.0],
            'description': ['Description 1', 'Description 2', 'Description 3'],
            'seller_info': ['Seller 1', 'Seller 2', 'Seller 1']
        }
        df = pd.DataFrame(data)

        output_path = os.path.join(self.output_dir, "price_plot.png")
        result_path = self.plot_generator.generate_price_plot(df, output_path)

        self.assertTrue(os.path.exists(result_path))

    def test_generate_seller_plot(self):
        """Test generation of seller plot."""
        data = {
            'name': ['Product 1', 'Product 2', 'Product 3'],
            'price': [100.0, 200.0, 300.0],
            'description': ['Description 1', 'Description 2', 'Description 3'],
            'seller_info': ['Seller 1', 'Seller 2', 'Seller 1']
        }
        df = pd.DataFrame(data)

        output_path = os.path.join(self.output_dir, "seller_plot.png")
        result_path = self.plot_generator.generate_seller_plot(df, output_path)

        self.assertTrue(os.path.exists(result_path))

    def test_generate_price_plot_missing_column(self):
        """Test generation of price plot with missing column."""
        data = {
            'name': ['Product 1', 'Product 2', 'Product 3'],
            'description': ['Description 1', 'Description 2', 'Description 3'],
            'seller_info': ['Seller 1', 'Seller 2', 'Seller 1']
        }
        df = pd.DataFrame(data)

        output_path = os.path.join(self.output_dir, "price_plot.png")

        with self.assertRaises(ValueError):
            self.plot_generator.generate_price_plot(df, output_path)

    def test_generate_seller_plot_missing_column(self):
        """Test generation of seller plot with missing column."""
        data = {
            'name': ['Product 1', 'Product 2', 'Product 3'],
            'price': [100.0, 200.0, 300.0],
            'description': ['Description 1', 'Description 2', 'Description 3']
        }
        df = pd.DataFrame(data)

        output_path = os.path.join(self.output_dir, "seller_plot.png")

        with self.assertRaises(ValueError):
            self.plot_generator.generate_seller_plot(df, output_path)


if __name__ == '__main__':
    unittest.main()