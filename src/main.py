#!/usr/bin/env python3
"""
Main entry point for the Webscraper for Indiamart Data Analysis.

This script initializes the scraping, analysis, and visualization modules
and orchestrates the workflow.
"""

import argparse
import sys
import logging
import os
from typing import Optional, Tuple

# Add the project root to Python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.indiamart_scraper import IndiamartScraper
from scraper.data_storage import DataStorage
from analyzer.data_cleaner import DataCleaner
from analyzer.data_analyzer import DataAnalyzer
from models.scraped_data import ScrapedData
from models.analyzed_data import AnalyzedData

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def scrape_data(url: str, output_dir: str = "data/raw") -> Optional[ScrapedData]:
    """Scrape data from Indiamart URL.
     
    Args:
        url: URL to scrape
        output_dir: Directory to save scraped data
         
    Returns:
        ScrapedData object or None if scraping failed
    """
    try:
        logger.info(f"Starting scraping process for URL: {url}")
         
        # Initialize scraper
        scraper = IndiamartScraper()
         
        # Scrape the data
        scraped_data = scraper.scrape(url)
        logger.info(f"Number of products scraped: {len(scraped_data.products)}")

         
        if not scraped_data:
            logger.error("No data was scraped")
            return None
             
        # Save the scraped data
        storage = DataStorage(output_dir)
        result = storage.save_scraped_data(scraped_data)
        
        logger.info(f"Successfully scraped and saved data from {url}")
        logger.info(f"Saved files: {result}")
        return scraped_data
         
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        return None


def analyze_data(input_file: str, output_dir: str = "data/processed") -> Optional[AnalyzedData]:
    """Analyze scraped data.
    
    Args:
        input_file: Path to scraped data file
        output_dir: Directory to save analyzed data
        
    Returns:
        AnalyzedData object or None if analysis failed
    """
    try:
        logger.info(f"Starting analysis process for file: {input_file}")
        
        # Initialize cleaner and analyzer
        cleaner = DataCleaner()
        analyzer = DataAnalyzer()
        
        # Load and clean data
        cleaned_data = cleaner.clean(input_file)

        if cleaned_data is None or cleaned_data.empty:
            logger.error("No valid data after cleaning")
            return None

        # Save cleaned data
        storage = DataStorage(output_dir)
        cleaned_csv_path = storage.save_cleaned_data(cleaned_data)

        # Analyze the cleaned data
        analyzed_data = analyzer.analyze(cleaned_data)

        # Save analyzed data
        storage.save_analyzed_data(analyzed_data)
        
        logger.info(f"Successfully analyzed data from {input_file}")
        return analyzed_data
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return None


def run_dashboard(input_file: Optional[str] = None):
    """Run the interactive dashboard.

    Args:
        input_file: Optional path to analyzed data file
    """
    try:
        from src.visualizer.dashboard import Dashboard
        import pandas as pd

        logger.info("Starting dashboard...")

        dashboard = Dashboard()

        if input_file:
            # Load the analyzed data
            analysis_results = pd.read_json(input_file)
            dashboard.run(analysis_results)
        else:
            # Run dashboard with empty data
            dashboard.run()

    except Exception as e:
        logger.error(f"Error running dashboard: {str(e)}")


def run_main():
    """Wrapper function to run main from project root."""
    main()


def main():
    """Main function to execute the webscraper workflow."""
    print("Webscraper for Indiamart Data Analysis")
    print("======================================")
    print("Initializing...")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Webscraper for Indiamart Data Analysis')
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scrape command
    scrape_parser = subparsers.add_parser('scrape', help='Scrape data from Indiamart')
    scrape_parser.add_argument('--url', required=True, help='URL to scrape from Indiamart')
    scrape_parser.add_argument('--output', default='data/raw', help='Output directory for scraped data')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze scraped data')
    analyze_parser.add_argument('--input', required=True, help='Input file with scraped data')
    analyze_parser.add_argument('--output', default='data/processed', help='Output directory for analyzed data')
    
    # Visualize command
    visualize_parser = subparsers.add_parser('visualize', help='Generate visualizations')
    visualize_parser.add_argument('--input', required=True, help='Input file with analyzed data')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Run interactive dashboard')
    dashboard_parser.add_argument('--input', help='Input file with analyzed data')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute the appropriate command
    if args.command == 'scrape':
        scrape_data(args.url, args.output)
    elif args.command == 'analyze':
        analyze_data(args.input, args.output)
    elif args.command == 'visualize':
        # Visualization will be handled by dashboard
        print("Visualization is now integrated into the dashboard. Use 'dashboard' command.")
    elif args.command == 'dashboard':
        run_dashboard(args.input)
    else:
        parser.print_help()


if __name__ == "__main__":
    run_main()