# Test Cases

## Unit Tests

Unit tests focus on individual functions or methods within each module.

### Scraper Module
1. **Test HTML Parsing**
   - **Function**: `parse_product_html(html_content)`
   - **Input**: Sample HTML string with product details.
   - **Expected Output**: Dictionary with extracted fields (name, price, etc.).
   - **Assertions**: Check that all fields are correctly parsed, handle missing tags.

2. **Test Rate Limiting**
   - **Function**: `apply_delay()`
   - **Input**: None
   - **Expected Output**: Delay applied without errors.
   - **Assertions**: Verify delay duration is within configured range.

3. **Test URL Generation**
   - **Function**: `generate_category_urls(categories)`
   - **Input**: List of categories (e.g., ['machinery', 'electronics']).
   - **Expected Output**: List of valid URLs.
   - **Assertions**: URLs match expected format for target sites.

### Data Processor Module
1. **Test Data Cleaning**
   - **Function**: `clean_data(df)`
   - **Input**: Pandas DataFrame with duplicates and missing values.
   - **Expected Output**: Cleaned DataFrame.
   - **Assertions**: No duplicates, missing values handled (e.g., filled or dropped).

2. **Test Price Standardization**
   - **Function**: `standardize_price(price_str)`
   - **Input**: String like "$100" or "₹5000".
   - **Expected Output**: Float value.
   - **Assertions**: Correct conversion, handle different currencies.

3. **Test Data Validation**
   - **Function**: `validate_data(df)`
   - **Input**: DataFrame with some invalid rows.
   - **Expected Output**: Boolean or list of valid rows.
   - **Assertions**: Invalid rows flagged or removed.

### EDA Module
1. **Test Statistics Calculation**
   - **Function**: `calculate_summary_stats(df)`
   - **Input**: Sample DataFrame.
   - **Expected Output**: Dictionary with mean, median, etc.
   - **Assertions**: Values match manual calculations.

2. **Test Visualization Data Generation**
   - **Function**: `generate_histogram_data(df, column)`
   - **Input**: DataFrame and column name.
   - **Expected Output**: Data for plotting.
   - **Assertions**: Correct binning and counts.

3. **Test Keyword Extraction**
   - **Function**: `extract_keywords(descriptions)`
   - **Input**: List of product descriptions.
   - **Expected Output**: List of top keywords.
   - **Assertions**: Keywords are relevant and ranked correctly.

## Integration Tests

Integration tests verify the interaction between modules and the end-to-end workflow.

1. **Scraping to Processing Pipeline**
   - **Scenario**: Run scraper on mock site, process data.
   - **Input**: Configuration file with mock URLs.
   - **Expected Output**: Cleaned data file.
   - **Assertions**: Data is scraped, processed, and stored correctly; no errors in logs.

2. **Processing to EDA Pipeline**
   - **Scenario**: Load processed data, perform analysis.
   - **Input**: Pre-processed data file.
   - **Expected Output**: Analysis report and plots.
   - **Assertions**: Statistics computed, visualizations generated.

3. **End-to-End Workflow**
   - **Scenario**: Full run from scraping to reporting.
   - **Input**: Full configuration.
   - **Expected Output**: Complete output directory with data, reports, and visuals.
   - **Assertions**: All steps execute without failure; output meets quality criteria (e.g., data completeness, insight accuracy).