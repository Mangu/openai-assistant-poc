import os
import requests
import logging
from dotenv import load_dotenv

# Create a custom logger
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('app.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_company_info(company_stock_ticker: str, question: str): 
    load_dotenv(".env")
    api_url = os.getenv("COMPANY_API_ENDPOINT")
    api_key = os.getenv("COMPANY_API_KEY")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }       
    payload = {
        'client': company_stock_ticker,
        'question': question
    }

    logger.info(f"Getting company information for {company_stock_ticker} with question {question}")
    response = requests.post(api_url, json=payload, headers=headers)

    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        chunks = [item['chunk'] for item in data['documents']]
        logger.info(f"Company info for {company_stock_ticker} found: {chunks}")        
        combined_chunks = ' '.join(chunks)
        return combined_chunks
    else:
        logger.info(f"Company info for {company_stock_ticker} not found") 
        return f"Company info for {company_stock_ticker} not found" 