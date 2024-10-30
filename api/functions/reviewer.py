import os
from openai import AzureOpenAI 
import logging
from dotenv import load_dotenv

# Create a custom logger
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('app.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

load_dotenv(".env")

print("got here")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-07-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

def review_chart(chart: str):
    # Set up the OpenAI API parameters

   
    deployment_name = "gpt-4o"  
    api_version = "2024-06-01"  
    # Configure the OpenAI API client
   
    # Make a request to the Azure OpenAI deployment

    # Create a prompt for the OpenAI API
    prompt = f"Review the following patient chart and provide feedback \n\n{chart}"
    messages = [
        {"role": "system", "content": "You are a medical assistant."},
        {"role": "user", "content": f"Review the following patient chart and provide feedback \n\n{chart}"}
    ]
    # Make a request to the OpenAI API using ChatCompletion endpoint
    response = client.chat.completions.create(
        model="gpt-4o", # model = "deployment_name".
        messages=messages
)
    # Log the successful response
    logging.info(f"OpenAI API response: {response}")
    
    # Extract the response text
    review = response.choices[0].message.content
    

    
    return review