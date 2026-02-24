---
layout: default
title: "Browser Use Tutorial - Chapter 5: Data Extraction"
nav_order: 5
has_children: false
parent: Browser Use Tutorial
---

# Chapter 5: Data Extraction - Scraping and Extracting Structured Data

Welcome to **Chapter 5: Data Extraction - Scraping and Extracting Structured Data**. In this part of **Browser Use Tutorial: AI-Powered Web Automation Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Extract structured data from websites using intelligent scraping techniques, pattern recognition, and data formatting.

## Overview

Data extraction is a powerful capability of Browser Use, allowing agents to scrape websites and extract structured information. This chapter covers techniques for extracting data from various web sources and formatting it for different use cases.

## Basic Data Extraction

### Text and Content Extraction

```python
# basic_extraction.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def basic_content_extraction():
    """Extract basic text content from web pages"""

    agent = Agent(
        task="""
        Extract content from https://httpbin.org/html:

        1. Extract the main heading (H1)
        2. Extract all paragraph text
        3. Extract all links and their destinations
        4. Extract any list items or structured content
        5. Return the extracted data in a structured format

        Focus on clean, organized data extraction.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=15
    )

    result = await agent.run()
    print(f"Extracted Content: {result}")

    # Process structured data
    if hasattr(result, 'extracted_content') and result.extracted_content:
        for item in result.extracted_content:
            if 'heading' in item:
                print(f"Heading: {item['heading']}")
            if 'paragraphs' in item:
                print(f"Paragraphs: {len(item['paragraphs'])} found")
            if 'links' in item:
                print(f"Links: {len(item['links'])} found")

if __name__ == "__main__":
    asyncio.run(basic_content_extraction())
```

### Table Data Extraction

```python
# table_extraction.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def table_data_extraction():
    """Extract structured data from HTML tables"""

    agent = Agent(
        task="""
        Extract data from tables on web pages:

        1. Go to https://news.ycombinator.com/ (or any site with tabular data)
        2. Identify the main stories table
        3. Extract data from multiple rows:
           - Story titles
           - Scores/points
           - Number of comments
           - Usernames
        4. Structure the data as a list of dictionaries
        5. Return the top 10 stories with their metadata

        Focus on maintaining data relationships and structure.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=20,
        use_vision=True  # Helps with table structure recognition
    )

    result = await agent.run()
    print(f"Table Data: {result}")

    # Process extracted table data
    if hasattr(result, 'extracted_content') and result.extracted_content:
        stories = result.extracted_content.get('stories', [])
        print(f"\nTop Stories ({len(stories)} found):")
        for i, story in enumerate(stories[:5], 1):  # Show top 5
            print(f"{i}. {story.get('title', 'N/A')}")
            print(f"   Score: {story.get('score', 'N/A')}, Comments: {story.get('comments', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(table_data_extraction())
```

## Advanced Data Extraction

### Product Information Extraction

```python
# product_extraction.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def product_data_extraction():
    """Extract product information from e-commerce sites"""

    agent = Agent(
        task="""
        Extract product information from an e-commerce site:

        1. Go to a product listing page (search for "laptops" on any retailer)
        2. Extract data for multiple products:
           - Product names
           - Prices
           - Brands/manufacturers
           - Key specifications
           - Ratings/reviews
        3. Structure the data consistently
        4. Handle different product layouts and information density

        Focus on creating reusable product data structures.
        Extract from 5-10 products to demonstrate scalability.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=30,
        use_vision=True
    )

    result = await agent.run()
    print(f"Product Data: {result}")

    # Process product data
    if hasattr(result, 'extracted_content') and result.extracted_content:
        products = result.extracted_content.get('products', [])
        print(f"\nExtracted {len(products)} products:")

        for product in products[:3]:  # Show first 3
            print(f"Name: {product.get('name', 'N/A')}")
            print(f"Price: {product.get('price', 'N/A')}")
            print(f"Brand: {product.get('brand', 'N/A')}")
            print("---")

if __name__ == "__main__":
    asyncio.run(product_data_extraction())
```

### News and Article Extraction

```python
# news_extraction.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def news_article_extraction():
    """Extract news articles and their content"""

    agent = Agent(
        task="""
        Extract news articles from a news website:

        1. Go to https://news.ycombinator.com/ or similar news site
        2. Identify 3-5 interesting articles
        3. For each article, extract:
           - Full title
           - Author/submitter
           - Article URL
           - Discussion/comments count
           - Any summary or excerpt text
        4. Click into one article and extract the full content
        5. Return structured article data

        Focus on content quality and completeness.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=35,
        use_vision=True
    )

    result = await agent.run()
    print(f"News Extraction: {result}")

    # Process news data
    if hasattr(result, 'extracted_content') and result.extracted_content:
        articles = result.extracted_content.get('articles', [])
        print(f"\nExtracted {len(articles)} articles:")

        for article in articles:
            print(f"Title: {article.get('title', 'N/A')}")
            print(f"Author: {article.get('author', 'N/A')}")
            print(f"Comments: {article.get('comments', 'N/A')}")
            print(f"URL: {article.get('url', 'N/A')}")
            print("---")

if __name__ == "__main__":
    asyncio.run(news_article_extraction())
```

## Structured Data Formats

### JSON Data Extraction

```python
# json_extraction.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
import json

async def json_data_extraction():
    """Extract and work with JSON data from web pages"""

    agent = Agent(
        task="""
        Extract JSON data from web APIs and format it properly:

        1. Go to https://httpbin.org/json
        2. Extract the JSON response
        3. Parse and understand the data structure
        4. Go to https://jsonplaceholder.typicode.com/users
        5. Extract the user data array
        6. Transform the data into a clean, structured format
        7. Return both datasets in organized form

        Focus on data integrity and proper JSON handling.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=20
    )

    result = await agent.run()
    print(f"JSON Data: {result}")

    # Process JSON data
    if hasattr(result, 'extracted_content') and result.extracted_content:
        json_data = result.extracted_content.get('json_data', {})

        # Pretty print JSON
        print("\nFormatted JSON Data:")
        print(json.dumps(json_data, indent=2))

if __name__ == "__main__":
    asyncio.run(json_data_extraction())
```

### CSV and Spreadsheet Data

```python
# csv_extraction.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
import csv
import io

async def csv_data_extraction():
    """Extract and process CSV/spreadsheet data"""

    agent = Agent(
        task="""
        Extract CSV or tabular data from web pages:

        1. Find a webpage with CSV data or data tables
        2. Extract the tabular data
        3. Identify column headers
        4. Parse rows of data
        5. Validate data integrity
        6. Return structured dataset

        If you can't find CSV data, extract from any data table.
        Focus on maintaining data relationships and types.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=25,
        use_vision=True
    )

    result = await agent.run()
    print(f"CSV Data: {result}")

    # Process CSV-like data
    if hasattr(result, 'extracted_content') and result.extracted_content:
        table_data = result.extracted_content.get('table_data', {})
        headers = table_data.get('headers', [])
        rows = table_data.get('rows', [])

        print(f"\nExtracted table with {len(headers)} columns and {len(rows)} rows")

        if headers and rows:
            # Create CSV-like output
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            writer.writerows(rows[:5])  # Show first 5 rows

            print("CSV Preview:")
            print(output.getvalue())

if __name__ == "__main__":
    asyncio.run(csv_data_extraction())
```

## Multi-Page Data Collection

### Pagination Handling

```python
# pagination_extraction.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def pagination_data_extraction():
    """Extract data across multiple pages"""

    agent = Agent(
        task="""
        Extract data across multiple pages (pagination):

        1. Go to a site with paginated content (news, products, search results)
        2. Extract data from the first page
        3. Navigate to the next page
        4. Extract data from the second page
        5. Continue for 2-3 more pages
        6. Combine all extracted data
        7. Remove duplicates if any
        8. Return consolidated dataset

        Focus on maintaining data consistency across pages.
        Use https://news.ycombinator.com/ with the "More" link for pagination.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=50,
        use_vision=True
    )

    result = await agent.run()
    print(f"Pagination Data: {result}")

    # Process paginated data
    if hasattr(result, 'extracted_content') and result.extracted_content:
        all_data = result.extracted_content.get('paginated_data', [])
        print(f"\nCollected data from {len(all_data)} pages")

        total_items = sum(len(page.get('items', [])) for page in all_data)
        print(f"Total items extracted: {total_items}")

if __name__ == "__main__":
    asyncio.run(pagination_data_extraction())
```

### Infinite Scroll Data

```python
# infinite_scroll_extraction.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def infinite_scroll_extraction():
    """Extract data from infinite scroll pages"""

    agent = Agent(
        task="""
        Extract data from infinite scroll pages:

        1. Find a page with infinite scroll (social media, news feeds, etc.)
        2. Start at the top and extract initial content
        3. Scroll down to load more content
        4. Continue scrolling and extracting until you have substantial data
        5. Monitor for when new content stops loading
        6. Return comprehensive dataset

        This tests handling dynamic content loading patterns.
        Look for sites like social media feeds or continuous content streams.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=40,
        use_vision=True
    )

    result = await agent.run()
    print(f"Infinite Scroll Data: {result}")

    # Analyze scroll performance
    if hasattr(result, 'metadata') and result.metadata:
        scrolls = result.metadata.get('scrolls_performed', 0)
        items_loaded = result.metadata.get('items_loaded', 0)
        print(f"Scrolls performed: {scrolls}")
        print(f"Items loaded: {items_loaded}")

if __name__ == "__main__":
    asyncio.run(infinite_scroll_extraction())
```

## Data Quality and Validation

### Data Cleaning and Validation

```python
# data_validation.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def data_quality_validation():
    """Extract and validate data quality"""

    agent = Agent(
        task="""
        Extract data with quality validation:

        1. Extract a dataset from a web page
        2. Validate data quality for each field:
           - Check for missing/null values
           - Validate data types (numbers, dates, strings)
           - Check for reasonable value ranges
           - Identify potential duplicates
           - Flag suspicious or invalid data

        3. Clean and normalize the data where possible
        4. Report data quality metrics
        5. Return cleaned, validated dataset

        Focus on creating reliable, high-quality extracted data.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=30
    )

    result = await agent.run()
    print(f"Validated Data: {result}")

    # Analyze data quality
    if hasattr(result, 'extracted_content') and result.extracted_content:
        quality_report = result.extracted_content.get('quality_report', {})
        print(f"\nData Quality Report:")
        print(f"Total records: {quality_report.get('total_records', 0)}")
        print(f"Valid records: {quality_report.get('valid_records', 0)}")
        print(f"Invalid records: {quality_report.get('invalid_records', 0)}")
        print(f"Completeness: {quality_report.get('completeness_percentage', 0)}%")

if __name__ == "__main__":
    asyncio.run(data_quality_validation())
```

### Duplicate Detection and Removal

```python
# duplicate_handling.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def duplicate_data_handling():
    """Handle duplicate data in extraction"""

    agent = Agent(
        task="""
        Extract data and handle duplicates intelligently:

        1. Extract data from multiple sources or pages
        2. Identify duplicate entries based on key fields
        3. Decide deduplication strategy:
           - Keep most complete record
           - Merge complementary information
           - Flag conflicts for manual review

        4. Remove duplicates while preserving data integrity
        5. Report deduplication results
        6. Return clean, deduplicated dataset

        This is common when scraping from multiple pages or sources.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=35
    )

    result = await agent.run()
    print(f"Deduplicated Data: {result}")

    # Analyze deduplication results
    if hasattr(result, 'extracted_content') and result.extracted_content:
        dedup_report = result.extracted_content.get('deduplication_report', {})
        print(f"\nDeduplication Report:")
        print(f"Original records: {dedup_report.get('original_count', 0)}")
        print(f"Unique records: {dedup_report.get('unique_count', 0)}")
        print(f"Duplicates removed: {dedup_report.get('duplicates_removed', 0)}")

if __name__ == "__main__":
    asyncio.run(duplicate_data_handling())
```

## Export and Integration

### Data Export Formats

```python
# data_export.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
import json
import csv

async def data_export_formats():
    """Extract data and export in multiple formats"""

    agent = Agent(
        task="""
        Extract data and prepare it for different export formats:

        1. Extract structured data from a web page
        2. Organize it into a consistent schema
        3. Prepare for multiple export formats:
           - JSON for API consumption
           - CSV for spreadsheet analysis
           - XML for enterprise systems
           - Markdown for documentation

        4. Ensure data is properly formatted for each target system
        5. Return data in all prepared formats

        Focus on format compatibility and data integrity.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=25
    )

    result = await agent.run()

    if hasattr(result, 'extracted_content') and result.extracted_content:
        data = result.extracted_content.get('structured_data', [])

        # Export to different formats
        if data:
            # JSON export
            with open('exported_data.json', 'w') as f:
                json.dump(data, f, indent=2)

            # CSV export (assuming tabular data)
            if data and isinstance(data[0], dict):
                headers = list(data[0].keys())
                with open('exported_data.csv', 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)

            print("Data exported to JSON and CSV formats")

    print(f"Export Result: {result}")

if __name__ == "__main__":
    asyncio.run(data_export_formats())
```

### API Integration

```python
# api_integration.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
import requests

async def api_data_integration():
    """Extract data and send to external APIs"""

    agent = Agent(
        task="""
        Extract data and integrate with external APIs:

        1. Extract product or business data from a website
        2. Transform the data to match target API schema
        3. Validate data before sending
        4. Send data to a mock API endpoint
        5. Handle API responses and potential errors
        6. Report integration results

        Use httpbin.org as your target API for testing.
        Focus on data transformation and error handling.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=30
    )

    result = await agent.run()

    # Simulate API integration
    if hasattr(result, 'extracted_content') and result.extracted_content:
        extracted_data = result.extracted_content.get('api_data', [])

        # Send to mock API
        for item in extracted_data[:3]:  # Send first 3 items
            try:
                response = requests.post(
                    'https://httpbin.org/post',
                    json=item,
                    timeout=10
                )
                print(f"API Response: {response.status_code}")
            except Exception as e:
                print(f"API Error: {e}")

    print(f"API Integration Result: {result}")

if __name__ == "__main__":
    asyncio.run(api_data_integration())
```

## Summary

In this chapter, we've covered:

- **Basic Content Extraction**: Text, links, and structured content
- **Table Data Extraction**: HTML tables and structured data
- **Advanced Extraction**: Products, news articles, and complex data
- **Structured Formats**: JSON, CSV, and various data formats
- **Multi-Page Collection**: Pagination and infinite scroll handling
- **Data Quality**: Validation, cleaning, and duplicate handling
- **Export Integration**: Multiple formats and API integration

## Key Takeaways

1. **Structured Extraction**: Focus on creating well-organized, typed data
2. **Multi-Page Handling**: Navigate pagination and infinite scroll effectively
3. **Data Quality**: Validate, clean, and deduplicate extracted data
4. **Format Flexibility**: Support multiple export formats for different use cases
5. **Scalability**: Handle large datasets and complex extraction scenarios
6. **Integration Ready**: Prepare data for API consumption and system integration
7. **Error Handling**: Robust handling of extraction failures and edge cases

## Next Steps

Now that you can extract structured data from websites, let's explore **multi-tab workflows** for handling complex browser automation scenarios.

---

**Ready for Chapter 6?** [Multi-Tab Workflows](06-multi-tab.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `result`, `print`, `Extract` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Data Extraction - Scraping and Extracting Structured Data` as an operating subsystem inside **Browser Use Tutorial: AI-Powered Web Automation Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `extracted_content`, `asyncio`, `Agent` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Data Extraction - Scraping and Extracting Structured Data` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `result`.
2. **Input normalization**: shape incoming data so `print` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Extract`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Browser Use Repository](https://github.com/browser-use/browser-use)
  Why it matters: authoritative reference on `Browser Use Repository` (github.com).
- [Browser Use Releases](https://github.com/browser-use/browser-use/releases)
  Why it matters: authoritative reference on `Browser Use Releases` (github.com).
- [Browser Use Docs](https://docs.browser-use.com/)
  Why it matters: authoritative reference on `Browser Use Docs` (docs.browser-use.com).
- [Browser Use Cloud](https://cloud.browser-use.com/)
  Why it matters: authoritative reference on `Browser Use Cloud` (cloud.browser-use.com).

Suggested trace strategy:
- search upstream code for `result` and `print` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Form Automation - Intelligent Form Filling and Submission](04-form-automation.md)
- [Next Chapter: Chapter 6: Multi-Tab Workflows - Managing Complex Multi-Tab Operations](06-multi-tab.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
