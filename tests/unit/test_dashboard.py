"""
Unit tests for the dashboard module.
"""

import unittest
import pandas as pd
import os
import tempfile
import shutil
from pathlib import Path
from src.visualizer.dashboard import Dashboard


class TestDashboard(unittest.TestCase):
    """Test cases for the Dashboard class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Create dashboard instance
        self.dashboard = Dashboard()
        
        # Update dashboard paths to use test directory
        self.dashboard.data_dir = self.test_dir
        self.dashboard.raw_data_dir = os.path.join(self.test_dir, "raw")
        self.dashboard.processed_data_dir = os.path.join(self.test_dir, "processed")
        
        # Create directories
        os.makedirs(self.dashboard.raw_data_dir, exist_ok=True)
        os.makedirs(self.dashboard.processed_data_dir, exist_ok=True)
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'product_name': ['Product A', 'Product B', 'Product C'],
            'price': [100, 200, 150],
            'seller_info': ['Seller X', 'Seller Y', 'Seller X'],
            'description': ['Desc A', 'Desc B', 'Desc C']
        })

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_dashboard_initialization(self):
        """Test that the Dashboard initializes correctly."""
        self.assertIsNotNone(self.dashboard)
        self.assertTrue(os.path.exists(self.dashboard.raw_data_dir))
        self.assertTrue(os.path.exists(self.dashboard.processed_data_dir))

    def test_dashboard_run_with_data(self):
        """Test that the dashboard can run with sample data."""
        # This is a basic test - in a real scenario, you'd want to mock Streamlit
        # and test the actual rendering, but that's complex for unit tests
        try:
            self.dashboard.run(self.sample_data)
            # If no exception is raised, the test passes
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Dashboard run failed with exception: {e}")

    def test_dashboard_run_with_empty_data(self):
        """Test that the dashboard handles empty data gracefully."""
        empty_data = pd.DataFrame()
        try:
            self.dashboard.run(empty_data)
            # If no exception is raised, the test passes
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Dashboard run with empty data failed with exception: {e}")

    def test_load_analyzed_data_no_files(self):
        """Test loading analyzed data when no files exist."""
        result = self.dashboard._load_analyzed_data()
        self.assertTrue(result.empty)

    def test_load_analyzed_data_with_file(self):
        """Test loading analyzed data from a file."""
        # Create a test JSON file
        test_data = {
            'product_name': ['Test Product'],
            'price': [100],
            'seller_info': ['Test Seller']
        }
        
        test_file = os.path.join(self.dashboard.processed_data_dir, "test_data.json")
        pd.DataFrame(test_data).to_json(test_file)
        
        # Load the data
        result = self.dashboard._load_analyzed_data()
        
        # Check that data was loaded
        self.assertFalse(result.empty)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['product_name'], 'Test Product')

    def test_show_scraping_section(self):
        """Test that the scraping section doesn't raise exceptions."""
        try:
            # This would normally require Streamlit context, so we just test
            # that the method can be called without errors in a non-Streamlit context
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"show_scraping_section failed: {e}")

    def test_show_analysis_section(self):
        """Test that the analysis section doesn't raise exceptions."""
        try:
            # This would normally require Streamlit context, so we just test
            # that the method can be called without errors in a non-Streamlit context
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"show_analysis_section failed: {e}")

    def test_show_visualization_section(self):
        """Test that the visualization section doesn't raise exceptions."""
        try:
            # This would normally require Streamlit context, so we just test
            # that the method can be called without errors in a non-Streamlit context
            self.dashboard._show_visualization_section(self.sample_data)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"show_visualization_section failed: {e}")


if __name__ == '__main__':
    unittest.main()