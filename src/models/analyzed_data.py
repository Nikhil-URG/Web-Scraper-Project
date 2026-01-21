"""
AnalyzedData model for the Webscraper for Indiamart Data Analysis.

This module defines the AnalyzedData class, which represents processed data
derived from the scraped data.
"""


class AnalyzedData:
    """Represents processed data derived from the scraped data."""

    def __init__(self, trends: dict, patterns: dict, statistics: dict, descriptive_analysis: dict = None,
                 price_analysis: dict = None, category_analysis: dict = None, seller_analysis: dict = None,
                 text_analysis: dict = None, correlation_analysis: dict = None, market_trends: dict = None,
                 outliers: dict = None, geographical_insights: dict = None, competitive_analysis: dict = None,
                 demand_indicators: dict = None, clustering: dict = None, time_series: dict = None,
                 sentiment_analysis: dict = None, inventory_analysis: dict = None, data_quality: dict = None):
        """Initialize an AnalyzedData instance.

        Args:
            trends: Identified trends in the data.
            patterns: Identified patterns in the data.
            statistics: Calculated statistics from the data.
            descriptive_analysis: Summary statistics for numerical fields.
            price_analysis: Price-related insights.
            category_analysis: Product category insights.
            seller_analysis: Seller-related insights.
            text_analysis: NLP insights from descriptions.
            correlation_analysis: Correlations between attributes.
            market_trends: Market trend insights.
            outliers: Outlier detection results.
            geographical_insights: Location-based insights.
            competitive_analysis: Competitive positioning.
            demand_indicators: Demand-related metrics.
            clustering: Product clustering results.
            time_series: Time-based analysis.
            sentiment_analysis: Sentiment from text.
            inventory_analysis: Inventory gaps and saturation.
            data_quality: Data quality metrics.
        """
        self.trends = trends
        self.patterns = patterns
        self.statistics = statistics
        self.descriptive_analysis = descriptive_analysis or {}
        self.price_analysis = price_analysis or {}
        self.category_analysis = category_analysis or {}
        self.seller_analysis = seller_analysis or {}
        self.text_analysis = text_analysis or {}
        self.correlation_analysis = correlation_analysis or {}
        self.market_trends = market_trends or {}
        self.outliers = outliers or {}
        self.geographical_insights = geographical_insights or {}
        self.competitive_analysis = competitive_analysis or {}
        self.demand_indicators = demand_indicators or {}
        self.clustering = clustering or {}
        self.time_series = time_series or {}
        self.sentiment_analysis = sentiment_analysis or {}
        self.inventory_analysis = inventory_analysis or {}
        self.data_quality = data_quality or {}

    def __repr__(self) -> str:
        """Return a string representation of the AnalyzedData."""
        return f"AnalyzedData(trends={self.trends}, patterns={self.patterns}, statistics={self.statistics}, ...)"


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

