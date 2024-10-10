import os
import openai
import logging
from dotenv import load_dotenv

# Create a custom logger
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('app.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def review_chart2(patient_chart: str):
    import openai
import os
from dotenv import load_dotenv
import logging

def review_chart2(patient_chart: str):
    # Load environment variables from .env file
    load_dotenv(".env")

    # Set up the OpenAI client
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai.api_base = os.getenv('AZURE_OPENAI_ENDPOINT')
    openai.api_type = "azure"
    openai.api_version = "2024-06-01"  # Corrected this line
    deployment_name = "gpt-4o"  # Assuming this is correct

    # Create a prompt for the OpenAI API
    prompt = f"Review the following patient chart and provide a summary:\n\n{patient_chart}"

    try:
        # Make a request to the OpenAI API using ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            engine=deployment_name,  # Specify the deployment name
            messages=[
                {"role": "system", "content": "You are a medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the response text
        review = response['choices'][0]['message']['content'].strip()
    except openai.error.InvalidRequestError as e:
        logging.error(f"InvalidRequestError: {e}")
        review = str(e)

    return review


def review_chart(patient_chart: str):
    # Set up the OpenAI API parameters

      
    
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    deployment_name = "gpt-4o"  
    api_version = "2024-06-01"  
    # Configure the OpenAI API client
    openai.api_type = "azure"
    openai.api_base = endpoint
    openai.api_version = api_version
    openai.api_key = api_key
    # Make a request to the Azure OpenAI deployment

    prompt = f"Review the following patient chart and provide a summary:\n\n{patient_chart}"
    def generate_response(prompt):
        response = openai.ChatCompletion.create(
            deployment_id=1,  # Specify the deployment name here
            prompt="what is the capital of france" # Adjust the token limit as per your requirements
        )
        return response
    
    return generate_response(prompt)
   
    
