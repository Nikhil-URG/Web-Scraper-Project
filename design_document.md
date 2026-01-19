# Design Document for Data Engineering Challenge

## 1. Design Process

### 1.1 Requirements Analysis
- **Objective**: Build a data gathering application for B2B marketplaces like IndiaMART and Alibaba, followed by exploratory data analysis.
- **Part A - Data Collection**:
  - Extract relevant product information from selected categories (e.g., industrial machinery, electronics, textiles).
  - Implement a robust crawler/scraper that respects site structures and avoids blocking.
  - Output clean, structured data in JSON/CSV format.
- **Part B - EDA**:
  - Perform statistical analysis, identify trends, and generate visualizations.
  - Uncover insights such as top product types, price distributions, regional patterns.
- **Evaluation Criteria**: Effectiveness, code quality, data structure, visualizations, insights.

### 1.2 Technology Selection
- **Programming Language**: Python - Widely used for data engineering, rich ecosystem for scraping and analysis.
- **Scraping Framework**: Scrapy - Asynchronous, handles large-scale crawling, built-in middleware for rate limiting and user agents.
- **Data Processing**: Pandas - For data manipulation and cleaning.
- **Visualization**: Matplotlib and Seaborn - For charts and plots.
- **Storage**: Local JSON/CSV files for simplicity; could extend to database if needed.
- **Testing**: Pytest for unit and integration tests.
- **Version Control**: Git for code management.

### 1.3 Architecture Design
- **Modular Structure**: Separate concerns into scraper, data processor, and analyzer modules.
- **Scalability**: Design for extensibility to add more sites or categories.
- **Error Handling**: Implement retries, logging, and graceful failure handling.
- **Data Flow**: Scrape → Clean/Process → Store → Analyze → Visualize.

### 1.4 Data Flow Design
1. **Input**: Configuration with target sites, categories, and parameters.
2. **Scraping**: Crawl pages, extract data fields (name, price, supplier, location, description).
3. **Processing**: Validate, clean, and structure data.
4. **Storage**: Save to files.
5. **Analysis**: Load data, compute statistics, generate plots.
6. **Output**: Reports and visualizations.

### 1.5 Error Handling and Robustness
- **Rate Limiting**: Use delays between requests, rotate user agents and proxies.
- **Retries**: Exponential backoff for failed requests.
- **Logging**: Comprehensive logging for debugging and monitoring.
- **Data Validation**: Check for missing fields, handle inconsistencies.

## 2. Architecture

### 2.1 High-Level Architecture
The system is divided into three main components:
- **Scraper Module**: Handles web crawling and data extraction.
- **Data Processor Module**: Cleans and structures the scraped data.
- **EDA Module**: Performs analysis and generates visualizations.

### 2.2 Component Details
- **Scraper**:
  - Uses Scrapy spiders to navigate sites.
  - Extracts fields using CSS/XPath selectors.
  - Handles pagination and category filtering.
- **Data Processor**:
  - Uses Pandas for data cleaning (remove duplicates, handle missing values).
  - Standardizes formats (e.g., currency, dates).
- **EDA**:
  - Computes summary statistics (mean, median, distributions).
  - Identifies top categories, price ranges, keywords.
  - Generates plots (histograms, bar charts, geographical maps).

### 2.3 Data Model
- **Scraped Data Schema**:
  - product_name: string
  - price: float
  - supplier: string
  - location: string
  - category: string
  - description: string
  - url: string
- Stored in JSON array or CSV.

### 2.4 Dependencies and Environment
- Python 3.8+
- Libraries: scrapy, pandas, matplotlib, seaborn, requests
- Environment: Virtual environment for dependency management.