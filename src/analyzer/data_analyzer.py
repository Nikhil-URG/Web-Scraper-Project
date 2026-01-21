"""
Data Analyzer for the Webscraper for Indiamart Data Analysis.

This module provides comprehensive functionality to analyze cleaned data and derive insights.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from collections import Counter
import re
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

# Download NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from src.models.analyzed_data import AnalyzedData


class DataAnalyzer:
    """Analyzes cleaned data and derives insights."""

    def __init__(self):
        """Initialize the DataAnalyzer."""
        pass

    def analyze(self, df: pd.DataFrame) -> AnalyzedData:
        """Analyze the DataFrame and derive comprehensive insights.

        Args:
            df: DataFrame containing the cleaned product data.

        Returns:
            AnalyzedData: An instance containing the analyzed data.
        """
        if df.empty:
            raise ValueError("DataFrame is empty")

        # Basic analyses
        trends = self._identify_trends(df)
        patterns = self._identify_patterns(df)
        statistics = self._calculate_statistics(df)

        # Comprehensive analyses
        descriptive_analysis = self._descriptive_analysis(df)
        price_analysis = self._price_analysis(df)
        category_analysis = self._category_analysis(df)
        seller_analysis = self._seller_analysis(df)
        text_analysis = self._text_analysis(df)
        correlation_analysis = self._correlation_analysis(df)
        market_trends = self._market_trends(df)
        outliers = self._outlier_detection(df)
        geographical_insights = self._geographical_insights(df)
        competitive_analysis = self._competitive_analysis(df)
        demand_indicators = self._demand_indicators(df)
        clustering = self._clustering(df)
        time_series = self._time_series_analysis(df)
        sentiment_analysis = self._sentiment_analysis(df)
        inventory_analysis = self._inventory_analysis(df)
        data_quality = self._data_quality_checks(df)

        return AnalyzedData(
            trends=trends, patterns=patterns, statistics=statistics,
            descriptive_analysis=descriptive_analysis, price_analysis=price_analysis,
            category_analysis=category_analysis, seller_analysis=seller_analysis,
            text_analysis=text_analysis, correlation_analysis=correlation_analysis,
            market_trends=market_trends, outliers=outliers,
            geographical_insights=geographical_insights, competitive_analysis=competitive_analysis,
            demand_indicators=demand_indicators, clustering=clustering,
            time_series=time_series, sentiment_analysis=sentiment_analysis,
            inventory_analysis=inventory_analysis, data_quality=data_quality
        )

    def _descriptive_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate descriptive statistics for numerical fields."""
        analysis = {}
        numerical_cols = df.select_dtypes(include=[np.number]).columns

        for col in numerical_cols:
            analysis[col] = {
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'mode': float(df[col].mode().iloc[0]) if not df[col].mode().empty else None,
                'std_dev': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'range': float(df[col].max() - df[col].min()),
                'quartiles': {k: float(v) for k, v in df[col].quantile([0.25, 0.5, 0.75]).to_dict().items()},
                'skewness': float(df[col].skew()),
                'kurtosis': float(df[col].kurtosis())
            }

        # Distribution analysis for price
        if 'Price' in df.columns:
            hist_counts, hist_bins = np.histogram(df['Price'], bins=20)
            analysis['price_distribution'] = {
                'histogram_bins': hist_bins.tolist(),
                'histogram_counts': hist_counts.tolist()
            }

        return analysis

    def _price_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze price-related insights."""
        analysis = {}

        if 'Price' in df.columns and not df.empty:
            prices = df['Price'].dropna()

            # Most and least expensive products
            analysis['most_expensive'] = df.loc[df['Price'].idxmax()].to_dict()
            analysis['least_expensive'] = df.loc[df['Price'].idxmin()].to_dict()

            # Top 10 most expensive products
            top_10_expensive = df.nlargest(10, 'Price')
            analysis['top_10_expensive'] = top_10_expensive[['Name', 'Price']].to_dict('records')

            # Simple price range: lowest to highest
            analysis['price_range'] = {
                'lowest': float(prices.min()),
                'highest': float(prices.max()),
                'range': float(prices.max() - prices.min())
            }

            # Price trends (if timestamps available)
            if 'timestamp' in df.columns:
                df_sorted = df.sort_values('timestamp')
                analysis['price_trend'] = float(df_sorted['Price'].pct_change().mean())

        return analysis

    def _category_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze product categories."""
        analysis = {}

        # Common keywords found in industrial product data
        category_keywords = {
            'Pipes & Fittings': ['pipe', 'tube', 'fitting', 'connector', 'elbow', 'tee', 'coupling'],
            'Valves & Pumps': ['valve', 'pump', 'compressor', 'flow', 'pressure'],
            'Motors & Engines': ['motor', 'engine', 'drive', 'gearbox', 'transmission'],
            'Electrical': ['cable', 'wire', 'switch', 'panel', 'electrical', 'power'],
            'Tools & Equipment': ['tool', 'machine', 'equipment', 'instrument', 'gauge'],
            'Other': []
        }

        analysis['category_keywords'] = category_keywords

        # Categorize products based on names/descriptions
        if 'Name' in df.columns:
            categories = []
            for name in df['Name'].str.lower():
                category_found = 'Other'
                for cat, keywords in category_keywords.items():
                    if cat != 'Other' and any(keyword in str(name) for keyword in keywords):
                        category_found = cat
                        break
                categories.append(category_found)

            df_copy = df.copy()
            df_copy['category'] = categories

            category_counts = df_copy['category'].value_counts()
            analysis['categories'] = {k: int(v) for k, v in category_counts.to_dict().items()}

            if 'Price' in df.columns:
                avg_prices = df_copy.groupby('category')['Price'].mean()
                analysis['avg_price_by_category'] = {k: float(v) for k, v in avg_prices.to_dict().items()}

        return analysis

    def _seller_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze seller-related insights."""
        analysis = {}

        if 'Seller Info' in df.columns:
            seller_counts = df['Seller Info'].value_counts()
            analysis['seller_product_counts'] = {k: int(v) for k, v in seller_counts.to_dict().items()}
            analysis['top_sellers'] = {k: int(v) for k, v in seller_counts.head(10).to_dict().items()}

            if 'Price' in df.columns:
                avg_prices = df.groupby('Seller Info')['Price'].mean()
                analysis['avg_price_by_seller'] = {k: float(v) for k, v in avg_prices.to_dict().items()}

        return analysis

    def _text_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform NLP analysis on product descriptions."""
        analysis = {}

        text_columns = [col for col in df.columns if 'description' in col.lower() or 'name' in col.lower()]

        if text_columns:
            all_text = ' '.join(df[text_columns[0]].dropna().astype(str))

            # Tokenize and remove stopwords
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(all_text.lower())
            filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

            # Most common keywords
            word_freq = Counter(filtered_words)
            analysis['common_keywords'] = dict(word_freq.most_common(20))

            # Extract features/specifications
            specs_pattern = r'\b\d+\s*(mm|cm|m|kg|ton|hp|watt|volt)\b'
            specs = re.findall(specs_pattern, all_text)
            analysis['specifications'] = dict(Counter(specs).most_common(10))

        return analysis

    def _correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between attributes."""
        analysis = {}

        numerical_df = df.select_dtypes(include=[np.number])
        if not numerical_df.empty:
            correlation_matrix = numerical_df.corr()
            analysis['correlation_matrix'] = correlation_matrix.to_dict()

            # Strong correlations
            strong_correlations = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr = correlation_matrix.iloc[i, j]
                    if abs(corr) > 0.5:
                        strong_correlations.append({
                            'var1': correlation_matrix.columns[i],
                            'var2': correlation_matrix.columns[j],
                            'correlation': float(corr)
                        })
            analysis['strong_correlations'] = strong_correlations

        return analysis

    def _market_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify market trends."""
        analysis = {}

        # Popular features from text analysis
        if 'text_analysis' in locals() or hasattr(self, '_text_analysis'):
            text_analysis = self._text_analysis(df)
            analysis['popular_features'] = text_analysis.get('common_keywords', {})

        # Product frequency trends
        if 'Name' in df.columns:
            product_freq = df['Name'].value_counts().head(10)
            analysis['popular_products'] = {k: int(v) for k, v in product_freq.to_dict().items()}

        return analysis

    def _outlier_detection(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers in the data."""
        analysis = {}

        if 'Price' in df.columns:
            prices = df['Price'].dropna()
            Q1 = prices.quantile(0.25)
            Q3 = prices.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = df[(df['Price'] < lower_bound) | (df['Price'] > upper_bound)]
            analysis['price_outliers'] = outliers.to_dict('records')

        return analysis

    def _geographical_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze geographical insights."""
        analysis = {}

        location_columns = [col for col in df.columns if 'location' in col.lower() or 'city' in col.lower() or 'state' in col.lower()]

        if location_columns:
            location_col = location_columns[0]
            location_counts = df[location_col].value_counts()
            analysis['seller_locations'] = {k: int(v) for k, v in location_counts.to_dict().items()}

            if 'Price' in df.columns:
                avg_prices = df.groupby(location_col)['Price'].mean()
                analysis['avg_price_by_location'] = {k: float(v) for k, v in avg_prices.to_dict().items()}

        return analysis

    def _competitive_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform competitive analysis."""
        analysis = {}

        if 'Name' in df.columns and 'Price' in df.columns and 'Seller Info' in df.columns:
            # Group by similar products
            product_groups = df.groupby(df['Name'].str.lower().str.split().str[:2].str.join(' '))

            competitive_products = {}
            for group_name, group in product_groups:
                if len(group) > 1:
                    competitive_products[str(group_name)] = {
                        'sellers': group['Seller Info'].tolist(),
                        'prices': [float(p) for p in group['Price'].tolist()],
                        'price_range': float(group['Price'].max() - group['Price'].min()),
                        'avg_price': float(group['Price'].mean())
                    }

            analysis['competitive_products'] = competitive_products

        return analysis

    def _demand_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze demand indicators."""
        analysis = {}

        # Look for views, ratings, sales columns
        demand_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['view', 'rating', 'sale', 'demand'])]

        if demand_cols and 'Price' in df.columns:
            for col in demand_cols:
                correlation = df[col].corr(df['Price']) if df[col].dtype in ['int64', 'float64'] else None
                analysis[f'{col}_price_correlation'] = float(correlation) if correlation is not None else None

        return analysis

    def _clustering(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform product clustering."""
        analysis = {}

        # Prepare data for clustering
        features = df.select_dtypes(include=[np.number]).dropna()

        if not features.empty and len(features) > 5:
            # Standardize features
            scaler = StandardScaler()
            scaled_features = scaler.fit_transform(features)

            # K-means clustering
            kmeans = KMeans(n_clusters=min(5, len(features)), random_state=42)
            clusters = kmeans.fit_predict(scaled_features)

            df_copy = df.copy()
            df_copy['cluster'] = clusters

            analysis['cluster_centers'] = kmeans.cluster_centers_.tolist()
            analysis['cluster_labels'] = clusters.tolist()
            analysis['cluster_sizes'] = np.bincount(clusters).tolist()

        return analysis

    def _time_series_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform time-series analysis."""
        analysis = {}

        time_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]

        if time_cols and 'Price' in df.columns:
            time_col = time_cols[0]
            df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
            df_time = df.dropna(subset=[time_col]).sort_values(time_col)

            # Price changes over time
            price_over_time = df_time.groupby(time_col)['Price'].mean()
            analysis['price_over_time'] = {str(k): float(v) for k, v in price_over_time.to_dict().items()}

        return analysis

    def _sentiment_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform sentiment analysis on text."""
        analysis = {}

        text_columns = [col for col in df.columns if 'description' in col.lower() or 'review' in col.lower()]

        if text_columns:
            sentiments = []
            for text in df[text_columns[0]].dropna().astype(str):
                blob = TextBlob(text)
                sentiments.append(blob.sentiment.polarity)

            analysis['average_sentiment'] = float(np.mean(sentiments))
            analysis['sentiment_distribution'] = {
                'positive': int(sum(1 for s in sentiments if s > 0.1)),
                'neutral': int(sum(1 for s in sentiments if -0.1 <= s <= 0.1)),
                'negative': int(sum(1 for s in sentiments if s < -0.1))
            }

        return analysis

    def _inventory_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze inventory gaps and saturation."""
        analysis = {}

        if 'Name' in df.columns:
            product_counts = df['Name'].value_counts()

            # Oversaturated categories (many similar products)
            oversaturated = product_counts[product_counts > product_counts.quantile(0.75)]
            analysis['oversaturated_products'] = {k: int(v) for k, v in oversaturated.to_dict().items()}

            # Potential gaps (categories with few products)
            undersaturated = product_counts[product_counts < product_counts.quantile(0.25)]
            analysis['potential_gaps'] = {k: int(v) for k, v in undersaturated.to_dict().items()}

        return analysis

    def _data_quality_checks(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform data quality checks."""
        analysis = {}

        try:
            # Missing data
            missing_data = df.isnull().sum()
            analysis['missing_values'] = {k: int(v) for k, v in missing_data[missing_data > 0].to_dict().items()}

            # Duplicate rows
            analysis['duplicate_rows'] = int(df.duplicated().sum())

            # Inconsistent data
            if 'Price' in df.columns:
                negative_prices = (df['Price'] < 0).sum()
                analysis['negative_prices'] = int(negative_prices)

            # Data completeness
            total_cells = df.shape[0] * df.shape[1]
            if total_cells > 0:
                analysis['completeness_score'] = float(1 - df.isnull().sum().sum() / total_cells)
            else:
                analysis['completeness_score'] = 0.0

            analysis['total_rows'] = int(df.shape[0])
            analysis['total_columns'] = int(df.shape[1])

        except Exception as e:
            analysis['error'] = str(e)

        return analysis

    # Legacy methods for backward compatibility
    def _identify_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify trends in the data."""
        return self._market_trends(df)

    def _identify_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify patterns in the data."""
        return self._category_analysis(df)

    def _calculate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate statistics from the data."""
        return self._descriptive_analysis(df)