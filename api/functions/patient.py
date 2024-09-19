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

def get_patient_chart(patient_name: str): 
    load_dotenv(".env")

    
def get_patient_information(patient_name: str): 
    load_dotenv(".env")
    
    