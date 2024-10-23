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

def search_protocol(question: str): 
    load_dotenv(".env")
    #url = os.getenv("BLS_API_ENDPOINT") 
    url ="https://pa-bls-mxvxk.swedencentral.inference.ml.azure.com/score"   
    #api_key = os.getenv("BLS_API_KEY")
    api_key = "vr0NrTVEFSADqR5AeDlDR0tR1flT6xfd"
    

    print(api_key)
        
    headers = {
        'Content-Type': 'application/json',
        'Authorization':('Bearer '+ api_key)
    }       
    payload = {
        'query': question
    }

    logger.info(f"Searching protocol at {url}")
    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        msg = data
        logger.info(f"Searching for {question} found: {data}")      
        return msg
    else:
        logger.info(f"Searching for {question} not found") 
        return "No data found" 