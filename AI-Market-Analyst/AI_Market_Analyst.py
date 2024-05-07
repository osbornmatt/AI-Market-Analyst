#!/usr/bin/env python
# coding: utf-8

import os
import yfinance as yf
from textwrap import dedent
from datetime import datetime
from openai import OpenAI
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

# System prompt definition
system_prompt = dedent("""
    You are a stock market analyzer. Your job is to receive input as follows:
    {{
        "Rate_Movement": float,
        "Market_Data": string
    }}
    where "Rate_Movement" are basis points (bps) showing how the 10 Year Treasury Rate changed during the day.
    "Market_Data" represents the market data for the day

    Your job is to use the information from "Market_Data" which can possibly explain the "Rate_Movement" and return an explanation using most of the "Market_Data" information. Do not add any preamble.
    Make sure your response is an HTML formatted bullet list, your response should therefore be in the following format:
    <ul>
        <li><strong>Short Heading</strong>: explanation point 1</li>
        <li><strong>Short Heading</strong>: explanation point 2</li>
        <li><strong>Short Heading</strong>: explanation point 3</li>
    </ul>
""")

# Function to query OpenAI
def query_openAI(text, model="gpt-3.5-turbo"):
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content

# Function to fetch the 10-year Treasury Bond rate
def get_10yr_bond_rate():
    bond = yf.Ticker("^TNX")  # ^TNX is the ticker for the 10-Year Treasury Note Yield
    hist = bond.history(period="7d")  # Get the latest daily data
    return hist['Close']  # Return the last closing price, which represents the current yield

# Function to scrape HTML content asynchronously
def scraper_with_AsyncHTMLLoader(url):
    loader = AsyncHtmlLoader(url, default_parser="html5lib")
    docs = loader.load()
    soup = BeautifulSoup(docs[0].page_content, 'html5lib')
    specific_sections = soup.find_all('section', class_='w-full')
    return specific_sections[0]

# Function to schedule jobs for market reporting
def job():
    hist = get_10yr_bond_rate()
    movement = (hist[-1]-hist[-2])*100
    data = scraper_with_AsyncHTMLLoader('https://www.edwardjones.ca/ca-en/market-news-insights/stock-market-news/daily-market-recap')
    
    response = query_openAI(dedent(f"""
                                {{
                                    "Rate_Movement": {movement}
                                    "Market_Data": {data}
                                }}
                            """),
                            #model='gpt-4-turbo'
                            )
    
    content = dedent(f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                            <title>AI Treasury Bond Market Report</title>
                        </head>
                        <body>
                            <div class="container mt-5">
                                <h2 class="mb-4">Market Report - {datetime.now().strftime("%B %d") }</h2>
        
                                <div class="card">
                                    <div class="card-header">
                                        <h3>10 Year Rate</h3>
                                    </div>
                                    <div class="card-body">
                                        <p><strong>Previous Close:</strong> <span class="badge bg-secondary">{hist[-2]:.2f}%</span></p>
                                        <p><strong>Today's Close:</strong> <span class="badge bg-primary">{hist[-1]:.2f}%</span></p>
                                        <p><strong>Movement:</strong> <span class="badge bg-info">{movement:.1f} bps</span></p>
                                    </div>
                                </div>

                                <div class="card mt-4">
                                    <div class="card-header">
                                        <h3>Analysis</h3>
                                    </div>
                                    <div class="card-body">
                                        {response}
                                    </div>
                                </div>
                            </div>
                        </body>
                        </html>
    """)
    
    # Open a file for writing
    file_name = f'Morning Market Report - {datetime.now().strftime("%B %d")}.html'
    with open(file_name, 'w') as file:
        # Write the string to the file
        file.write(content)

    # Automatically open the file with the default application
    os.startfile(file_name)

# Main execution block
if __name__ == '__main__':
    load_dotenv()  # Load environment variables from .env
    job()