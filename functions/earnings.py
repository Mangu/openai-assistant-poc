import os
import requests
import logging

# Create a custom logger
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('app.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_earnings_call_transcript(company_name: str):         
    source_url = os.getenv("STOCK_API_URL")    
    url = f"{source_url}/{company_name}"  

    logger.info(f"Getting earnings call at {url}")

    response = requests.get(url)   
    if response.status_code == 200:        
        data = response.json()
        logger.info(f"Earnings call for {company_name} found: {data}") 

        #msg = (f"application: {application}, host: {host}, jvm: {jvm}, ip: {ip}, port: {port}")   
        msg = data       
        return msg
    else:
        logger.info(f"Earning call for {company_name} not found") 
        return None  