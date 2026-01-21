"""
AnalyzedData model for the Webscraper for Indiamart Data Analysis.

This module defines the AnalyzedData class, which represents processed data
derived from the scraped data.
"""


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

