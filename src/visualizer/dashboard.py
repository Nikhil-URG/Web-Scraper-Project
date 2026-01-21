"""
Dashboard for the Webscraper for Indiamart Data Analysis.

This module provides functionality to create a dashboard for visualizing analyzed data
and integrating the scraping workflow.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import sys
import os
import json
from pathlib import Path


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

    def _load_analyzed_data(self) -> pd.DataFrame:
        """Load cleaned data from the processed directory.

        Returns:
            DataFrame with cleaned data or empty DataFrame if no data found
        """
        try:
            # Find the latest cleaned data file
            cleaned_files = list(Path(self.processed_data_dir).glob("cleaned_data.csv"))

            if not cleaned_files:
                return pd.DataFrame()

            # Use the most recent file
            latest_file = max(cleaned_files, key=lambda x: x.stat().st_mtime)

            # Load the CSV file
            df = pd.read_csv(latest_file)
            return df

        except Exception as e:
            st.error(f"Error loading cleaned data: {str(e)}")
            return pd.DataFrame()

    def _show_scraping_section(self):
        """Show the scraping section of the dashboard."""
        st.header("🔍 Web Scraping")
        
        with st.form("scraping_form"):
            url = st.text_input("Enter Indiamart URL to scrape:", 
                              placeholder="https://dir.indiamart.com/impcat/pvc-pipes.html")
            
            submit_button = st.form_submit_button("Start Scraping")
            
            if submit_button and url:
                if url.startswith("https://www.indiamart.com/") or url.startswith("https://dir.indiamart.com/"):
                    with st.spinner("Scraping data..."):
                        success = self._run_scraping_command(url)
                         
                        if success:
                            # Show available scraped files
                            scraped_files = list(Path(self.raw_data_dir).glob("*.csv"))
                            if scraped_files:
                                st.subheader("Scraped Data Files")
                                for file in sorted(scraped_files, key=lambda x: x.stat().st_mtime, reverse=True):
                                    st.code(str(file))
                else:
                    st.error("Please enter a valid Indiamart URL starting with 'https://dir.indiamart.com/' or 'https://www.indiamart.com/'")

    def _show_analysis_section(self):
        """Show the analysis section of the dashboard."""
        st.header("📊 Data Analysis")
        
        # Check if there are scraped files available
        scraped_files = list(Path(self.raw_data_dir).glob("*.csv"))
        
        if scraped_files:
            st.info(f"Found {len(scraped_files)} scraped data file(s) ready for analysis.")
            
            if st.button("Analyze Data"):
                with st.spinner("Analyzing data..."):
                    success = self._run_analysis_command()
                    
                    if success:
                        # Show available analyzed files
                        analyzed_files = list(Path(self.processed_data_dir).glob("*.json"))
                        if analyzed_files:
                            st.subheader("Analyzed Data Files")
                            for file in sorted(analyzed_files, key=lambda x: x.stat().st_mtime, reverse=True):
                                st.code(str(file))
        else:
            st.warning("No scraped data available. Please scrape data first.")

    def _show_visualization_section(self, df: pd.DataFrame):
        """Show the visualization section of the dashboard.
        
        Args:
            df: DataFrame containing the analyzed data
        """
        st.header("📈 Data Visualization")

        if df.empty:
            st.warning('No analyzed data available for visualization. Please scrape and analyze data first.')
            return

        # Show data overview
        st.subheader("Data Overview")
        st.write(df.head())
        
        # Show statistics
        st.subheader("Data Statistics")
        st.write(df.describe())

        # Price Distribution
        st.subheader('Price Distribution')
        if 'Price' in df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['Price'], bins=20, color='blue', alpha=0.7, edgecolor='black')
            ax.set_title('Distribution of Product Prices', fontsize=14, fontweight='bold')
            ax.set_xlabel('Price', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        # Top Sellers
        st.subheader('Top Sellers')
        if 'Seller Info' in df.columns:
            seller_counts = df['Seller Info'].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(10, 6))
            seller_counts.plot(kind='bar', ax=ax, color='green', alpha=0.7, edgecolor='black')
            ax.set_title('Top 10 Sellers by Product Count', fontsize=14, fontweight='bold')
            ax.set_xlabel('Seller', fontsize=12)
            ax.set_ylabel('Number of Products', fontsize=12)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)

        # Additional visualizations
        if 'Name' in df.columns and 'Price' in df.columns:
            st.subheader('Product Price Comparison')

            # Show top 10 most expensive products
            top_expensive = df.nlargest(10, 'Price')
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(top_expensive['Name'], top_expensive['Price'], color='purple', alpha=0.7)
            ax.set_title('Top 10 Most Expensive Products', fontsize=14, fontweight='bold')
            ax.set_xlabel('Price', fontsize=12)
            ax.set_ylabel('Product Name', fontsize=12)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

    def run(self, df: pd.DataFrame):
        """Run the Streamlit dashboard.

        Args:
            df: DataFrame containing the analyzed data.
        """
        st.set_page_config(
            page_title="Indiamart Data Analysis Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title('🚀 Indiamart Data Analysis Dashboard')
        st.markdown("""
        Welcome to the Indiamart Data Analysis Dashboard!
        
        This dashboard allows you to:
        1. **Scrape** product data from Indiamart
        2. **Analyze** the scraped data to extract insights
        3. **Visualize** the analyzed data with interactive charts
        """)

        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Select a section:",
            ["Scraping", "Analysis", "Visualization"]
        )

        # Load analyzed data
        analyzed_df = self._load_analyzed_data()

        # Show appropriate section based on navigation
        if page == "Scraping":
            self._show_scraping_section()
        elif page == "Analysis":
            self._show_analysis_section()
        elif page == "Visualization":
            # Use the provided df if available, otherwise use loaded analyzed data
            visualization_df = df if not df.empty else analyzed_df
            self._show_visualization_section(visualization_df)
        
        # Footer
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        ### About
        **Indiamart Data Analysis Dashboard**
        
        Version: 1.0.0
        
        A comprehensive tool for scraping, analyzing, and visualizing
        product data from Indiamart.
        """)