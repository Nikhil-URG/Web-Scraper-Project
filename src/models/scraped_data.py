"""
ScrapedData model for the Webscraper for Indiamart Data Analysis.

This module defines the ScrapedData class, which represents raw data
collected from Indiamart.
"""


class ScrapedData:
    """Represents raw data collected from Indiamart."""

    def __init__(self, url: str, products: list, metadata: dict):
        """Initialize a ScrapedData instance.

        Args:
            url: URL from which the data was scraped.
            products: List of Product instances.
            metadata: Additional metadata about the scraping process.
        """
        self.url = url
        self.products = products
        self.metadata = metadata

    def __repr__(self) -> str:
        """Return a string representation of the ScrapedData."""
        return f"ScrapedData(url='{self.url}', products={self.products}, metadata={self.metadata})"


class AnalyzedData:
    """Represents processed data derived from the scraped data."""

    def __init__(self, trends: dict, patterns: dict, statistics: dict):
        """Initialize an AnalyzedData instance.

        Args:
            trends: Identified trends in the data.
            patterns: Identified patterns in the data.
            statistics: Calculated statistics from the data.
        """
        self.trends = trends
        self.patterns = patterns
        self.statistics = statistics

    def __repr__(self) -> str:
        """Return a string representation of the AnalyzedData."""
        return f"AnalyzedData(trends={self.trends}, patterns={self.patterns}, statistics={self.statistics})"


class Visualization:
    """Represents graphical representation of the analyzed data."""

    def __init__(self, graph_data: dict, plot_data: dict, trend_lines: dict):
        """Initialize a Visualization instance.

        Args:
            graph_data: Data for generating graphs.
            plot_data: Data for generating plots.
            trend_lines: Data for generating trend lines.
        """
        self.graph_data = graph_data
        self.plot_data = plot_data
        self.trend_lines = trend_lines

    def __repr__(self) -> str:
        """Return a string representation of the Visualization."""
        return f"Visualization(graph_data={self.graph_data}, plot_data={self.plot_data}, trend_lines={self.trend_lines})"