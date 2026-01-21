"""
Product model for the Webscraper for Indiamart Data Analysis.

This module defines the Product class, which represents a product
listed on Indiamart.
"""


class Product:
    """Represents a product listed on Indiamart."""

    def __init__(self, name: str, price: float, description: str, seller_info: str):
        """Initialize a Product instance.

        Args:
            name: Name of the product.
            price: Price of the product.
            description: Description of the product.
            seller_info: Information about the seller.
        """
        self.name = name
        self.price = price
        self.description = description
        self.seller_info = seller_info

    def __repr__(self) -> str:
        """Return a string representation of the Product."""
        return f"Product(name='{self.name}', price={self.price}, description='{self.description}', seller_info='{self.seller_info}')"