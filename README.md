# Webscraper for Indiamart Data Analysis

A comprehensive web scraping and data analysis tool for extracting product information from Indiamart and generating insights.

## Features

- **Web Scraping**: Extract product data from Indiamart including names, prices, descriptions, and seller information
- **Data Analysis**: Clean, process, and analyze scraped data to identify trends and patterns
- **Visualization**: Generate interactive dashboards and visualizations of the analyzed data
- **Data Storage**: Save scraped data in structured formats (CSV, JSON)

## Project Structure

```
webscraper-indiamart/
├── src/
│   ├── main.py                  # Main entry point
│   ├── models/
│   │   ├── product.py           # Product model
│   │   ├── scraped_data.py      # Scraped data model
│   │   └── analyzed_data.py     # Analyzed data model
│   ├── scraper/
│   │   ├── indiamart_scraper.py # Indiamart scraping logic
│   │   └── data_storage.py      # Data storage functionality
│   ├── analyzer/
│   │   ├── data_cleaner.py      # Data cleaning and preprocessing
│   │   └── data_analyzer.py     # Data analysis and insights
│   └── visualizer/
│       ├── plot_generator.py    # Plot generation
│       └── dashboard.py         # Interactive dashboard
├── tests/
│   ├── unit/
│   │   ├── test_scraper.py      # Scraper unit tests
│   │   ├── test_analyzer.py     # Analyzer unit tests
│   │   └── test_visualizer.py   # Visualizer unit tests
│   └── integration/
│       └── test_integration.py  # Integration tests
├── data/
│   ├── raw/                    # Raw scraped data
│   ├── processed/               # Processed data
│   └── visualizations/          # Generated visualizations
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore patterns
└── README.md                   # Project documentation
```

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/webscraper-indiamart.git
cd webscraper-indiamart
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Scraper

To scrape data from Indiamart:

```bash
python src/main.py scrape --url "https://dir.indiamart.com/impcat/pvc-pipes.html"
```

### Running the Data Analyzer

To analyze scraped data:

```bash
python src/main.py analyze --input data/raw/scraped_data.csv
```

### Running the Visualizer

To generate visualizations:

```bash
python src/main.py visualize --input data/processed/analyzed_data.json
```

### Running the Dashboard

To start the interactive dashboard:

```bash
python src/main.py dashboard --input data/processed/analyzed_data.json
```

## Running Tests

### Unit Tests

```bash
pytest tests/unit/
```

### Integration Tests

```bash
pytest tests/integration/
```

### All Tests

```bash
pytest
```

### Test with Coverage

```bash
pytest --cov=src tests/
```

## Configuration

The project uses environment variables for configuration. Create a `.env` file in the project root:

```
# Scraper settings
SCRAPER_TIMEOUT=30
SCRAPER_RETRIES=3
SCRAPER_DELAY=2

# Data storage settings
DATA_DIR=data
RAW_DATA_DIR=data/raw
PROCESSED_DATA_DIR=data/processed
VISUALIZATIONS_DIR=data/visualizations

# Logging settings
LOG_LEVEL=INFO
LOG_FILE=webscraper.log
```

## Development

### Code Formatting

```bash
black src/ tests/
```

### Linting

```bash
flake8 src/ tests/
```

### Type Checking

```bash
mypy src/ tests/
```

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact:
- Email: support@webscraper-indiamart.com
- GitHub Issues: https://github.com/yourusername/webscraper-indiamart/issues

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you've activated the virtual environment and installed all dependencies.

2. **Scraping Failures**: Check your internet connection and verify the target URLs are accessible.

3. **Permission Errors**: Make sure the data directories exist and are writable.

### Debugging

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file or environment variables.

## Roadmap

- Add support for additional e-commerce platforms
- Implement machine learning for advanced trend analysis
- Add user authentication for the dashboard
- Implement scheduled scraping jobs
- Add export functionality for reports
