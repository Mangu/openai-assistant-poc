from azure.communication.email import EmailClient
import openai
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

def send_report(email_address, content):
    load_dotenv(".env")

    logger.info(f"Sending email for thread_id: {content} to {email_address}")

    try:        
        connection_string = os.getenv("EMAIL_CONNECTION_STRING")        
        client = EmailClient.from_connection_string(connection_string)
        senderAddress = os.getenv("EMAIL_FROM")
        summary = content

        message = {
            "senderAddress": senderAddress,
            "recipients":  {
                "to": [{"address": email_address}],
            },
            "content": {
                "subject": "EMS Buddy - Conversation Summary",
                "plainText": summary,
            }
        }       

        poller = client.begin_send(message)
        result = poller.result()

        if result.get('status') == "Succeeded":
            msg = "Email sent"
            logger.info(f"Email sent with:  {content} to {email_address}")
        else:
            msg = "Email not sent. Did you provide a valid email address?"
            logger.info(f"Email was not sent for thread_id:  {content} to {email_address} Status: {result.get('status')}")

        return msg

    except Exception as ex:
        logger.info(f"Error sending email for thread_id:  {content} to {email_address}. Error: {ex}")