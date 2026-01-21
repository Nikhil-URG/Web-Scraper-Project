"""
Plot Generator for the Webscraper for Indiamart Data Analysis.

This module provides functionality to generate plots from analyzed data.
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any


class PlotGenerator:
    """Generates plots from analyzed data."""

    def __init__(self):
        """Initialize the PlotGenerator."""
        pass

    def generate_price_plot(self, df: pd.DataFrame, output_path: str) -> str:
        """Generate a plot of product prices.

        Args:
            df: DataFrame containing the product data.
            output_path: Path to save the plot.

        Returns:
            str: Path to the saved plot.
        """
        if 'price' not in df.columns:
            raise ValueError("DataFrame does not contain 'price' column")

        plt.figure(figsize=(10, 6))
        plt.hist(df['price'], bins=20, color='blue', alpha=0.7)
        plt.title('Distribution of Product Prices')
        plt.xlabel('Price')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()

        return output_path

    def generate_seller_plot(self, df: pd.DataFrame, output_path: str) -> str:
        """Generate a plot of top sellers.

        Args:
            df: DataFrame containing the product data.
            output_path: Path to save the plot.

        Returns:
            str: Path to the saved plot.
        """
        if 'seller_info' not in df.columns:
            raise ValueError("DataFrame does not contain 'seller_info' column")

        seller_counts = df['seller_info'].value_counts().head(10)

        plt.figure(figsize=(10, 6))
        seller_counts.plot(kind='bar', color='green', alpha=0.7)
        plt.title('Top 10 Sellers by Product Count')
        plt.xlabel('Seller')
        plt.ylabel('Number of Products')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()

        return output_path