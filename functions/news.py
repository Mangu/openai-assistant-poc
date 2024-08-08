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

def get_news(company_stock_ticker: str): 

    load_dotenv(".env")
    url = os.getenv("NEWS_API_ENDPOINT") 
    
    
    headers = {
        'Content-Type': 'application/json'
    }       
    payload = {
        'client': company_stock_ticker
    }

    logger.info(f"Getting company news at {url}")
    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        msg = data['clientAINarrative'] 
        logger.info(f"Company news for {company_stock_ticker} found: {data}")      
        return msg
    else:
        logger.info(f"Company news for {company_stock_ticker} not found") 
        return None 