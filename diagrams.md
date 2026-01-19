# Architecture Diagrams

## High-Level Architecture Diagram

```mermaid
graph TD
    A[User Configuration] --> B[Scraper Module]
    B --> C[Data Processor Module]
    C --> D[Storage]
    D --> E[EDA Module]
    E --> F[Reports & Visualizations]

    B -->|Extracted Data| C
    C -->|Cleaned Data| D
    D -->|Data| E
```

## Data Flow Diagram

```mermaid
flowchart LR
    Start([Start]) --> Config[Load Configuration<br/>Sites, Categories]
    Config --> Scrape[Crawl & Scrape Data]
    Scrape --> Process[Clean & Process Data]
    Process --> Store[Store Data<br/>JSON/CSV]
    Store --> Analyze[Perform EDA<br/>Statistics, Insights]
    Analyze --> Visualize[Generate Visualizations<br/>Charts, Reports]
    Visualize --> End([End])
```

## Component Interaction Diagram

```mermaid
graph LR
    subgraph Scraper
        S1[Scrapy Spider] --> S2[Data Extraction]
        S2 --> S3[Rate Limiting]
    end
    subgraph Processor
        P1[Pandas Cleaning] --> P2[Data Validation]
        P2 --> P3[Standardization]
    end
    subgraph EDA
        E1[Statistics Calculation] --> E2[Visualization]
        E2 --> E3[Insight Generation]
    end

    Scraper --> Processor
    Processor --> EDA