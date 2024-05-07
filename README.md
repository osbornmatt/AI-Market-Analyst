# Stock Market Analysis Tool

This Python script provides an automated way to analyze and report on stock market data, focusing on the 10-year Treasury bond rate. It utilizes several external libraries and APIs to fetch, process, and explain market data in relation to treasury rate movements.

## Features

- Fetches the latest 10-year Treasury bond rate.
- Scrapes market data from specified URLs asynchronously.
- Analyzes the correlation between market data and bond rate movements using the OpenAI GPT model.
- Generates a daily HTML report with the analysis and bond rate information.

## Installation

Before running the script, ensure you have Python installed on your system and then install the required dependencies:

```bash
pip install yfinance bs4 openai langchain-community dotenv
```

## Usage

The script is scheduled to run as a daily job. To start the script, simply execute it from the command line:

```bash
python stock_market_analysis.py
```

The script will:
- Fetch the latest 10-year Treasury bond rate.
- Scrape market data.
- Generate an analysis using the OpenAI model.
- Produce a comprehensive HTML report with the analyzed data, which automatically opens for viewing.

## Environment Variables

Make sure to set up the necessary environment variables in a `.env` file in the root directory:

- OPENAI_API_KEY: Your OpenAI API key for accessing GPT models.

## HTML Report

The generated HTML report will include:
- Current and previous 10-year Treasury bond rates.
- Detailed analysis in the form of an HTML bullet list explaining the potential causes of rate movements based on the market data.

## Dependencies

- `yfinance`: Used to fetch financial data.
- `beautifulsoup4` and `langchain-community`: Used for web scraping and HTML content processing.
- `openai`: Used to query the OpenAI API for generating explanations.
- `dotenv`: Used to manage environment variables.
- `warnings`: Used to suppress warnings.

## Author

Matt Osborn

## License

This project is licensed under the [MIT License](LICENSE).