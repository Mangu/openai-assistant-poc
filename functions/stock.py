import os
import requests
import logging
import json

# Create a custom logger
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('app.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_stock_info(company_stock_ticker):
    search_service_name = os.getenv("AZURE_AISEARCH_ENDPOINT")
    api_key = os.getenv("AZURE_AISEARCH_KEY")

    index_name='revenueinfo' 
    api_version='2020-06-30'  
    
    url = f"{search_service_name}/indexes/{index_name}/docs"
    logger.info(f"Getting stock information at {url}")
    params = {
        'api-version': api_version,
        'search': company_stock_ticker
    }
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    logger.info(f"Getting stock information for {company_stock_ticker}")  

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return json.dumps(response.json(), indent=4)
    else:        
        logger.info(f"Error getting stock info for {company_stock_ticker}")
        return f"Error: {response.status_code} getting stock info at: {url}"