import os
import requests
import logging
import json
from dotenv import load_dotenv

# Create a custom logger
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('app.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

load_dotenv(".env")

def search_protocol(question: str): 
    
    url = os.getenv("BLS_API_ENDPOINT")        
    api_key = os.getenv("BLS_API_KEY") 
    
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

        # Check if 'documents' and 'reply' keys exist
        if "documents" in data and "reply" in data:
            documents = data["documents"]
            # Extract file paths and reply
            file_paths = [doc["filepath"] for doc in documents]
            reply = data["reply"]

            # Concatenate file paths and reply into a single string
            result = "\n references: ".join(file_paths) + " \n response: " + reply
            logger.info(f"Searching for {question} found: {data}")
            return result
        else:
            result = "Error: 'documents' or 'reply' key not found in the JSON response."
    else:
        logger.info(f"Searching for {question} not found")
        result = "No data found"
