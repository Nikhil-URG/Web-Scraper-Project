"""
Data Cleaner for the Webscraper for Indiamart Data Analysis.

This module provides functionality to clean and preprocess scraped data.
"""

import pandas as pd
from typing import List

from src.models.product import Product


class DataCleaner:
    """Cleans and preprocesses scraped data."""

    def __init__(self):
        """Initialize the DataCleaner."""
        pass

    def clean(self, input_file: str) -> pd.DataFrame:
        """Clean data from a CSV file.

        Args:
            input_file: Path to the CSV file containing scraped data.

        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        try:
            # Read the CSV file
            df = pd.read_csv(input_file)

            # Basic cleaning
            df = df.dropna()  # Remove rows with NaN values
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0.0)
            df['Name'] = df['Name'].astype(str).str.strip()
            df['Description'] = df['Description'].astype(str).str.strip()
            df['Seller Info'] = df['Seller Info'].astype(str).str.strip()

            return df

        except Exception as e:
            print(f"Error cleaning data: {e}")
            return pd.DataFrame()

    def clean_products(self, products: List[Product]) -> List[Product]:
        """Clean the list of products.

        Args:
            products: List of Product instances to clean.

        Returns:
            List[Product]: Cleaned list of Product instances.
        """
        cleaned_products = []

        for product in products:
            # Example cleaning logic
            cleaned_name = product.name.strip() if product.name else "Unknown"
            cleaned_price = product.price if product.price > 0 else 0.0
            cleaned_description = product.description.strip() if product.description else "No description"
            cleaned_seller_info = product.seller_info.strip() if product.seller_info else "Unknown seller"

            cleaned_product = Product(
                name=cleaned_name,
                price=cleaned_price,
                description=cleaned_description,
                seller_info=cleaned_seller_info
            )
            cleaned_products.append(cleaned_product)

        return cleaned_products

    def to_dataframe(self, products: List[Product]) -> pd.DataFrame:
        """Convert a list of products to a pandas DataFrame.

        Args:
            products: List of Product instances.

        Returns:
            pd.DataFrame: DataFrame containing the product data.
        """
        data = {
            'name': [product.name for product in products],
            'price': [product.price for product in products],
            'description': [product.description for product in products],
            'seller_info': [product.seller_info for product in products]
        }

        return pd.DataFrame(data)