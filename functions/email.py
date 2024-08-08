from azure.communication.email import EmailClient
from openai import AzureOpenAI
import os
import re
from dotenv import load_dotenv
import logging

# Create a custom logger
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('app.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def send_summary(email_address, thread_id):
    load_dotenv(".env")

    logger.info(f"Sending email for thread_id: {thread_id} to {email_address}")

    try:        
        connection_string = os.getenv("EMAIL_CONNECTION_STRING")        
        client = EmailClient.from_connection_string(connection_string)
        senderAddress = os.getenv("EMAIL_FROM")
        summary = get_summary(thread_id)

        message = {
            "senderAddress": senderAddress,
            "recipients":  {
                "to": [{"address": email_address}],
            },
            "content": {
                "subject": "What's Happening - Conversation Summary",
                "plainText": summary,
            }
        }       

        poller = client.begin_send(message)
        result = poller.result()

        if result.get('status') == "Succeeded":
            msg = "Email sent"
            logger.info(f"Email sent for thread_id:  {thread_id} to {email_address}")
        else:
            msg = "Email not sent. Did you provide a valid email address?"
            logger.info(f"Email was not sent for thread_id:  {thread_id} to {email_address} Status: {result.get('status')}")

        return msg

    except Exception as ex:
        logger.info(f"Error sending email for thread_id:  {thread_id} to {email_address}. Error: {ex}")
        

def get_summary(thread):    
    api_key=os.getenv("AZURE_OPENAI_API_KEY")     
    azure_enpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  

    client = AzureOpenAI(
        api_key=api_key,  
        api_version="2024-02-15-preview",
        azure_endpoint = azure_enpoint
    )      

    messages = client.beta.threads.messages.list(thread_id=thread)

    all_messages = ""
    for message in reversed(messages.data):
        for content in reversed(message.content):
            if content.type == "text":
                text_value = content.text.value                
                text_value = re.sub(r"thread_id: \w+", "", text_value)                
                all_messages += text_value + "\n\n\n"
     
    return all_messages