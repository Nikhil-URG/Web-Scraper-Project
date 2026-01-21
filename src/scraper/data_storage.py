"""
Data Storage for the Webscraper for Indiamart Data Analysis.

This module provides functionality to store scraped data in a structured format.
"""

import csv
import os
import json
from typing import List

import pandas as pd

from src.models.product import Product
from src.models.scraped_data import ScrapedData
from src.models.analyzed_data import AnalyzedData


class DataStorage:
    """Stores scraped data in a structured format."""

    def __init__(self, output_dir: str = "data"):
        """Initialize the DataStorage.

        Args:
            output_dir: Directory to store the output files.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_scraped_data(self, scraped_data: ScrapedData) -> dict:
        """Save both CSV data and metadata for scraped data.
        
        Args:
            scraped_data: ScrapedData instance containing the data to save.
            
        Returns:
            dict: Dictionary with paths to saved files
        """
        result = {}
        
        # Save CSV data
        if scraped_data.products:
            csv_path = self.save_to_csv(scraped_data)
            result['csv_path'] = csv_path
        
        # Save metadata
        if scraped_data.metadata:
            metadata_path = self.save_metadata(scraped_data)
            result['metadata_path'] = metadata_path
            
        return result

    def save_to_csv(self, scraped_data: ScrapedData) -> str:
        """Save the scraped data to a CSV file.

        Args:
            scraped_data: ScrapedData instance containing the data to save.

        Returns:
            str: Path to the saved CSV file.
        """
        if not scraped_data.products:
            raise ValueError("No products to save")

        csv_path = os.path.join(self.output_dir, "scraped_data.csv")

        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Description', 'Seller Info'])

            for product in scraped_data.products:
                writer.writerow([
                    product.name,
                    product.price,
                    product.description,
                    product.seller_info
                ])

        return csv_path

    def save_metadata(self, scraped_data: ScrapedData) -> str:
        """Save the metadata to a JSON file.

        Args:
            scraped_data: ScrapedData instance containing the metadata to save.

        Returns:
            str: Path to the saved JSON file.
        """
        import json

        json_path = os.path.join(self.output_dir, "metadata.json")

        with open(json_path, mode='w', encoding='utf-8') as file:
            json.dump(scraped_data.metadata, file, indent=4)

        return json_path

    def save_cleaned_data(self, df: pd.DataFrame) -> str:
        """Save the cleaned DataFrame to a CSV file.

        Args:
            df: DataFrame containing the cleaned data.

        Returns:
            str: Path to the saved CSV file.
        """
        csv_path = os.path.join(self.output_dir, "cleaned_data.csv")
        df.to_csv(csv_path, index=False)
        return csv_path

    def save_analyzed_data(self, analyzed_data: AnalyzedData) -> str:
        """Save the analyzed data to a JSON file.

        Args:
            analyzed_data: AnalyzedData instance containing the data to save.

        Returns:
            str: Path to the saved JSON file.
        """
        json_path = os.path.join(self.output_dir, "analyzed_data.json")

        data = {
            "trends": analyzed_data.trends,
            "patterns": analyzed_data.patterns,
            "statistics": analyzed_data.statistics
        }

        with open(json_path, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        return json_path