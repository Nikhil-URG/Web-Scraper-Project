"""
Dashboard for the Webscraper for Indiamart Data Analysis.

This module provides functionality to create a dashboard for visualizing analyzed data
and integrating the scraping workflow.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import sys
import os
import json
from pathlib import Path

# Custom CSS for better styling
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem;
    }
    .sidebar-content {
        padding: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)


class Dashboard:
    """Creates a dashboard for visualizing analyzed data and managing the scraping workflow."""

    def __init__(self):
        """Initialize the Dashboard."""
        self.data_dir = "data"
        self.raw_data_dir = os.path.join(self.data_dir, "raw")
        self.processed_data_dir = os.path.join(self.data_dir, "processed")
        
        # Create directories if they don't exist
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)

    def _run_scraping_command(self, url: str) -> bool:
        """Run the scraping command using subprocess.
        
        Args:
            url: URL to scrape
            
        Returns:
            True if scraping was successful, False otherwise
        """
        try:
            # Run the scraping command
            result = subprocess.run([
                sys.executable, "src/main.py", "scrape",
                "--url", url,
                "--output", self.raw_data_dir
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                st.success(f"Scraping completed successfully!")
                st.text(f"Output: {result.stdout}")
                return True
            else:
                st.error(f"Scraping failed!")
                st.text(f"Error: {result.stderr}")
                # Also show the stdout which might contain additional error information
                if result.stdout:
                    st.text(f"Additional info: {result.stdout}")
                return False
                
        except Exception as e:
            st.error(f"Error running scraping command: {str(e)}")
            return False

    def _run_analysis_command(self) -> bool:
        """Run the analysis command using subprocess.
        
        Returns:
            True if analysis was successful, False otherwise
        """
        try:
            # Find the latest scraped file
            scraped_files = list(Path(self.raw_data_dir).glob("*.csv"))
            
            if not scraped_files:
                st.warning("No scraped data files found.")
                return False
                
            # Use the most recent file
            latest_file = max(scraped_files, key=lambda x: x.stat().st_mtime)
            
            # Run the analysis command
            result = subprocess.run([
                sys.executable, "src/main.py", "analyze",
                "--input", str(latest_file),
                "--output", self.processed_data_dir
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                st.success(f"Analysis completed successfully!")
                st.text(f"Output: {result.stdout}")
                return True
            else:
                st.error(f"Analysis failed!")
                st.text(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            st.error(f"Error running analysis command: {str(e)}")
            return False

    def _load_analyzed_data(self) -> tuple:
        """Load analyzed data from the processed directory.

        Returns:
            Tuple of (DataFrame with cleaned data, dict with analysis results) or (empty DataFrame, empty dict) if no data found
        """
        try:
            # Find the latest analyzed data file
            analyzed_files = list(Path(self.processed_data_dir).glob("analyzed_data.json"))

            if not analyzed_files:
                return pd.DataFrame(), {}

            # Use the most recent file
            latest_file = max(analyzed_files, key=lambda x: x.stat().st_mtime)

            # Load the JSON file
            with open(latest_file, 'r') as f:
                analysis_results = json.load(f)

            # Also try to load the cleaned data for raw data display
            cleaned_files = list(Path(self.processed_data_dir).glob("cleaned_data.csv"))
            if cleaned_files:
                latest_cleaned = max(cleaned_files, key=lambda x: x.stat().st_mtime)
                df = pd.read_csv(latest_cleaned)
            else:
                df = pd.DataFrame()

            return df, analysis_results

        except Exception as e:
            st.error(f"Error loading analyzed data: {str(e)}")
            return pd.DataFrame(), {}

    def _show_scraping_section(self):
        """Show the scraping section of the dashboard."""
        st.markdown('<h2 class="section-header">🔍 Web Scraping</h2>', unsafe_allow_html=True)

        with st.container():
            st.markdown("Enter a URL from Indiamart to scrape product data.")

            col1, col2 = st.columns([3, 1])
            with col1:
                url = st.text_input("Indiamart URL:",
                                   placeholder="https://dir.indiamart.com/impcat/pvc-pipes.html",
                                   label_visibility="collapsed")
            with col2:
                if st.button("🚀 Start Scraping", type="primary"):
                    if url and (url.startswith("https://www.indiamart.com/") or url.startswith("https://dir.indiamart.com/")):
                        with st.spinner("🔄 Scraping data... Please wait."):
                            success = self._run_scraping_command(url)

                            if success:
                                st.success("✅ Scraping completed successfully!")
                                # Show available scraped files
                                scraped_files = list(Path(self.raw_data_dir).glob("*.csv"))
                                if scraped_files:
                                    st.subheader("📁 Scraped Data Files")
                                    for file in sorted(scraped_files, key=lambda x: x.stat().st_mtime, reverse=True):
                                        st.code(str(file))
                    else:
                        st.error("❌ Please enter a valid Indiamart URL starting with 'https://dir.indiamart.com/' or 'https://www.indiamart.com/'")

    def _show_analysis_section(self):
        """Show the analysis section of the dashboard."""
        st.markdown('<h2 class="section-header">📊 Data Analysis</h2>', unsafe_allow_html=True)

        with st.container():
            # Check if there are scraped files available
            scraped_files = list(Path(self.raw_data_dir).glob("*.csv"))

            if scraped_files:
                st.info(f"📂 Found {len(scraped_files)} scraped data file(s) ready for analysis.")

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🔬 Analyze Data", type="primary", use_container_width=True):
                        with st.spinner("🔄 Analyzing data... This may take a moment."):
                            success = self._run_analysis_command()

                            if success:
                                st.success("✅ Analysis completed successfully!")
                                # Show available analyzed files
                                analyzed_files = list(Path(self.processed_data_dir).glob("*.json"))
                                if analyzed_files:
                                    st.subheader("📁 Analyzed Data Files")
                                    for file in sorted(analyzed_files, key=lambda x: x.stat().st_mtime, reverse=True):
                                        st.code(str(file))
            else:
                st.warning("⚠️ No scraped data available. Please scrape data first from the Scraping section.")

    def _show_visualization_section(self, df: pd.DataFrame, analysis_results: dict):
        """Show the comprehensive visualization section of the dashboard.

        Args:
            df: DataFrame containing the raw data
            analysis_results: Dictionary containing all analysis results
        """
        st.markdown('<h2 class="section-header">📈 Comprehensive Data Analysis & Visualization</h2>', unsafe_allow_html=True)

        if not analysis_results:
            st.warning('⚠️ No analyzed data available for visualization. Please scrape and analyze data first.')
            return

        # Executive Summary
        st.markdown("### 📊 Executive Summary")
        col1, col2, col3, col4 = st.columns(4)

        # Get metrics from analysis results
        descriptive_analysis = analysis_results.get('descriptive_analysis', {})
        price_analysis = analysis_results.get('price_analysis', {})
        seller_analysis = analysis_results.get('seller_analysis', {})
        data_quality = analysis_results.get('data_quality', {})

        with col1:
            total_products = data_quality.get('total_rows', len(df) if not df.empty else 0)
            st.metric("Total Products", total_products)

        with col2:
            avg_price = descriptive_analysis.get('Price', {}).get('mean', 0)
            st.metric("Average Price", f"₹{avg_price:.2f}")

        with col3:
            unique_sellers = len(seller_analysis.get('seller_product_counts', {}))
            st.metric("Unique Sellers", unique_sellers)

        with col4:
            completeness = data_quality.get('completeness_score', 0)
            st.metric("Data Quality", f"{completeness:.1%}")

        # Create tabs for different analysis categories
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Price Analysis", "🏪 Seller Analysis", "📂 Category Analysis", "📋 Data Quality"])

        with tab1:
            self._show_price_analysis(df, analysis_results)

        with tab2:
            self._show_seller_analysis(df, analysis_results)

        with tab3:
            self._show_category_analysis(df, analysis_results)

        with tab4:
            self._show_data_quality(analysis_results)

        # Raw Data Explorer
        with st.expander("📋 Raw Data Explorer", expanded=False):
            if not df.empty:
                st.write(df.head())
                st.write("**Descriptive Statistics:**")
                st.write(df.describe())
            else:
                st.write("No raw data available")

    def _show_price_analysis(self, df: pd.DataFrame, analysis_results: dict):
        """Show price-related visualizations."""
        st.markdown("#### 💰 Price Analysis")

        price_analysis = analysis_results.get('price_analysis', {})

        if 'Price' in df.columns and not df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader('Price Distribution')
                descriptive_analysis = analysis_results.get('descriptive_analysis', {})
                price_dist = descriptive_analysis.get('Price', {}).get('histogram_counts', [])
                price_bins = descriptive_analysis.get('Price', {}).get('histogram_bins', [])

                if price_dist and price_bins:
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(price_bins[:-1], price_dist, width=price_bins[1]-price_bins[0], color='#1f77b4', alpha=0.8, edgecolor='black')
                    ax.set_title('Distribution of Product Prices', fontsize=14, fontweight='bold')
                    ax.set_xlabel('Price (₹)', fontsize=12)
                    ax.set_ylabel('Frequency', fontsize=12)
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                elif not df.empty and 'Price' in df.columns:
                    # Fallback to calculating from df
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.hist(df['Price'], bins=30, color='#1f77b4', alpha=0.8, edgecolor='black')
                    ax.set_title('Distribution of Product Prices', fontsize=14, fontweight='bold')
                    ax.set_xlabel('Price (₹)', fontsize=12)
                    ax.set_ylabel('Frequency', fontsize=12)
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                else:
                    st.write("No price distribution data available")

            with col2:
                st.subheader('Price Range')
                price_range = price_analysis.get('price_range', {})
                if price_range:
                    st.metric("Lowest Price", f"₹{price_range.get('lowest', 0):.2f}")
                    st.metric("Highest Price", f"₹{price_range.get('highest', 0):.2f}")
                    st.metric("Price Range", f"₹{price_range.get('range', 0):.2f}")
                else:
                    st.write("No price range data available")
                    if analysis_results:
                        st.write("Available analysis keys:", list(analysis_results.keys()))
                        if 'price_analysis' in analysis_results:
                            price_analysis = analysis_results['price_analysis']
                            st.write("Price analysis keys:", list(price_analysis.keys()) if isinstance(price_analysis, dict) else "Not a dict")
                            st.write("Price analysis content:", price_analysis)

            # Top expensive products
            st.subheader('Top 10 Most Expensive Products')
            top_10_expensive = price_analysis.get('top_10_expensive', [])
            if top_10_expensive:
                # Display as table instead of chart
                expensive_df = pd.DataFrame({
                    'Product': [item['Name'][:50] for item in top_10_expensive],  # Truncate long names
                    'Price (₹)': [f"₹{item['Price']:.2f}" for item in top_10_expensive]
                })
                st.dataframe(expensive_df, use_container_width=True)
            else:
                st.write("No product price data available")

    def _show_seller_analysis(self, df: pd.DataFrame, analysis_results: dict):
        """Show seller-related visualizations."""
        st.markdown("#### 🏪 Seller Analysis")

        seller_analysis = analysis_results.get('seller_analysis', {})

        if 'Seller Info' in df.columns and not df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader('Top Sellers by Product Count')
                top_sellers = seller_analysis.get('top_sellers', {})
                if top_sellers:
                    # Display as table
                    seller_df = pd.DataFrame({
                        'Seller': list(top_sellers.keys()),
                        'Product Count': list(top_sellers.values())
                    })
                    st.dataframe(seller_df, use_container_width=True)
                else:
                    st.write("No seller data available")
                    if analysis_results:
                        st.write("Available analysis keys:", list(analysis_results.keys()))
                        if 'seller_analysis' in analysis_results:
                            st.write("Seller analysis content:", analysis_results['seller_analysis'])

            with col2:
                st.subheader('Average Price by Seller')
                avg_prices = seller_analysis.get('avg_price_by_seller', {})
                if avg_prices:
                    sellers = list(avg_prices.keys())[:10]
                    prices = [avg_prices[seller] for seller in sellers]
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.barh(sellers, prices, color='#d62728', alpha=0.8)
                    ax.set_title('Average Price by Top Sellers', fontsize=14, fontweight='bold')
                    ax.set_xlabel('Average Price (₹)', fontsize=12)
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                else:
                    st.write("No average price data available")
                    if analysis_results:
                        st.write("Available analysis keys:", list(analysis_results.keys()))
                        if 'seller_analysis' in analysis_results:
                            seller_analysis = analysis_results['seller_analysis']
                            st.write("Seller analysis keys:", list(seller_analysis.keys()) if isinstance(seller_analysis, dict) else "Not a dict")
                            st.write("Seller analysis content:", seller_analysis)

    def _show_category_analysis(self, df: pd.DataFrame, analysis_results: dict):
        """Show category-related visualizations."""
        st.markdown("#### 📂 Category Analysis")

        category_analysis = analysis_results.get('category_analysis', {})

        # Show keywords
        keywords = category_analysis.get('category_keywords', {})
        if keywords:
            st.subheader('Category Keywords Used')
            for category, words in keywords.items():
                st.write(f"**{category}**: {', '.join(words)}")

        categories = category_analysis.get('categories', {})
        if categories:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader('Product Categories Distribution')
                # Display as list/table instead of pie chart
                category_df = pd.DataFrame({
                    'Category': list(categories.keys()),
                    'Count': list(categories.values())
                })
                st.dataframe(category_df, use_container_width=True)

            with col2:
                st.subheader('Average Price by Category')
                avg_prices = category_analysis.get('avg_price_by_category', {})
                if avg_prices:
                    # Display as list/table instead of bar chart
                    price_df = pd.DataFrame({
                        'Category': list(avg_prices.keys()),
                        'Average Price (₹)': [f"₹{price:.2f}" for price in avg_prices.values()]
                    })
                    st.dataframe(price_df, use_container_width=True)

    def _show_advanced_insights(self, df: pd.DataFrame, analysis_results: dict):
        """Show advanced analysis visualizations."""
        st.markdown("#### 🔍 Advanced Insights")

        # Text Analysis
        text_analysis = analysis_results.get('text_analysis', {})
        if text_analysis.get('common_keywords'):
            st.subheader('Most Common Keywords')
            keywords = text_analysis['common_keywords']
            fig, ax = plt.subplots(figsize=(10, 6))
            words = list(keywords.keys())[:15]
            counts = list(keywords.values())[:15]
            ax.barh(words, counts, color='#8c564b', alpha=0.8)
            ax.set_title('Most Common Keywords in Product Descriptions', fontsize=14, fontweight='bold')
            ax.set_xlabel('Frequency', fontsize=12)
            st.pyplot(fig)

        # Correlation Analysis
        correlation_analysis = analysis_results.get('correlation_analysis', {})
        strong_correlations = correlation_analysis.get('strong_correlations', [])
        if strong_correlations:
            st.subheader('Strong Variable Correlations')
            corr_df = pd.DataFrame(strong_correlations)
            st.dataframe(corr_df)

        # Outlier Analysis
        outliers = analysis_results.get('outliers', {}).get('price_outliers', [])
        if outliers:
            st.subheader('Price Outliers Detected')
            outlier_df = pd.DataFrame(outliers)
            st.dataframe(outlier_df[['Name', 'Price', 'Seller Info']].head())

        # Sentiment Analysis
        sentiment_analysis = analysis_results.get('sentiment_analysis', {})
        if sentiment_analysis.get('sentiment_distribution'):
            st.subheader('Sentiment Analysis')
            sentiment_dist = sentiment_analysis['sentiment_distribution']
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(sentiment_dist.keys(), sentiment_dist.values(), color=['#d62728', '#7f7f7f', '#2ca02c'], alpha=0.8)
            ax.set_title('Sentiment Distribution in Descriptions', fontsize=14, fontweight='bold')
            ax.set_ylabel('Count', fontsize=12)
            st.pyplot(fig)

    def _show_data_quality(self, analysis_results: dict):
        """Show data quality metrics."""
        st.markdown("#### 📋 Data Quality Assessment")

        data_quality = analysis_results.get('data_quality', {})

        col1, col2, col3 = st.columns(3)

        with col1:
            completeness = data_quality.get('completeness_score', 0)
            st.metric("Data Completeness", f"{completeness:.1%}")

        with col2:
            duplicates = data_quality.get('duplicate_rows', 0)
            st.metric("Duplicate Rows", duplicates)

        with col3:
            missing_values = len(data_quality.get('missing_values', {}))
            st.metric("Columns with Missing Data", missing_values)

        # Debug info
        if not data_quality:
            st.write("No data quality information available")
            if analysis_results:
                st.write("Available analysis keys:", list(analysis_results.keys()))
                if 'data_quality' in analysis_results:
                    st.write("Data quality content:", analysis_results['data_quality'])

        if data_quality.get('missing_values'):
            st.subheader('Missing Values by Column')
            missing_df = pd.DataFrame(list(data_quality['missing_values'].items()), columns=['Column', 'Missing Count'])
            st.dataframe(missing_df)

    def run(self, df: pd.DataFrame = None):
        """Run the Streamlit dashboard.

        Args:
            df: Optional DataFrame or dict containing analyzed data from main.py
        """
        st.set_page_config(
            page_title="Indiamart Data Analysis Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Load custom CSS
        load_css()

        # Header with logo
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            try:
                st.image("public/FFFFFF-1.png", width=100)
            except:
                pass  # Logo not found
        with col2:
            st.markdown('<h1 class="main-header">🚀 Indiamart Data Analysis Dashboard</h1>', unsafe_allow_html=True)
        with col3:
            pass

        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
        Welcome to the Indiamart Data Analysis Dashboard!<br>
        This dashboard allows you to:
        <ul style="list-style-type: none; padding: 0;">
        <li>🔍 <strong>Scrape</strong> product data from Indiamart</li>
        <li>📊 <strong>Analyze</strong> the scraped data to extract insights</li>
        <li>📈 <strong>Visualize</strong> the analyzed data with beautiful charts</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        # Sidebar navigation
        with st.sidebar:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            st.title("🧭 Navigation")
            page = st.radio(
                "Select a section:",
                ["Scraping", "Analysis", "Visualization"],
                index=2 if df is not None else 0  # Default to Visualization if data provided
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Handle data loading
        if df is not None and isinstance(df, dict):
            # df is analysis_results from main.py
            analysis_results = df
            analyzed_df = pd.DataFrame()  # No raw data available
        else:
            # Load from processed directory
            analyzed_df, analysis_results = self._load_analyzed_data()
            if df is not None and not df.empty:
                analyzed_df = df  # Override with provided df

        # Show appropriate section based on navigation
        if page == "Scraping":
            self._show_scraping_section()
        elif page == "Analysis":
            self._show_analysis_section()
        elif page == "Visualization":
            self._show_visualization_section(analyzed_df, analysis_results)
        
        # Footer
        st.markdown("---")
        st.markdown('<div class="footer">', unsafe_allow_html=True)
        st.markdown("""
        ### About
        **Indiamart Data Analysis Dashboard** v1.0.0
        
        A comprehensive tool for scraping, analyzing, and visualizing product data from Indiamart.
        Built with ❤️ using Streamlit.
        """)
        st.markdown('</div>', unsafe_allow_html=True)