from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader, APIKey
from openai import AzureOpenAI
import os
import time
import json
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from functions.company import get_company_info
from functions.news import get_news
from functions.stock import get_stock_info
from functions.email import send_summary
from dotenv import load_dotenv
import logging

# Create a custom logger
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('app.log')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

load_dotenv(".env")

assistant_id = "asst_5N02i9PqB3VVqUYSAbkm76WH"
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

# Load API key from environment variable. This is used to authenticate requests to the API
API_KEY = os.getenv("FAST_API_KEY")

# Check for API key
if API_KEY is None:
    raise ValueError("API_KEY environment variable not set")

API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

app = FastAPI()

origins = [    
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class MessageRequest(BaseModel):
    message: str
    thread_id: str

class MessageResponse(BaseModel):
    message: str

class ThreadResponse(BaseModel):
    thread_id: str

#add the available functions here   
available_functions = {"get_company_info": get_company_info, "get_news": get_news, "get_stock_info": get_stock_info, "send_summary": send_summary}
def main_loop(run, thread_id):

    max_steps = 100
    sleep = 0.5
    
    try:
        cnt = 0
        while cnt < max_steps:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)        
            cnt += 1
            if run.status == "requires_action":
                tool_responses = []
                if (run.required_action.type == "submit_tool_outputs" and run.required_action.submit_tool_outputs.tool_calls is not None):
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls

                    for call in tool_calls:
                        if call.type == "function":                            
                            if call.function.name not in available_functions:
                                logger.info(f"Function not availble for thread_id: {thread_id} and run_id: {run.id}: {call.function.name}")
                                raise Exception("Function requested by the model does not exist")
                            function_to_call = available_functions[call.function.name]                            
                            tool_response = function_to_call(**json.loads(call.function.arguments))                           
                            tool_responses.append({"tool_call_id": call.id, "output": tool_response})
                            
                            logger.info(f"Function name for thread_id: {thread_id} and run_id: {run.id}: {call.function.name}") 
                            logger.info(f"Function args for thread_id: {thread_id} and run_id: {run.id}: {call.function.arguments}")  
                            
                    logger.info(f"Tool response for thread_id: {thread_id} and run_id: {run.id}: {tool_responses}")
                    run = client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run.id, tool_outputs=tool_responses)
            if run.status == "failed":
                logger.info(f"Run failed for threadid: {thread_id} and run_id: {run.id}")                 
                break
            if run.status == "completed":
                logger.info(f"Run completed for threadid: {thread_id} and run_id: {run.id}") 
                break
            #time.sleep(sleep)

    except Exception as e:
        logger.info(f"Errors for threadid: {thread_id} error: {e}")        

    return run

# Define the bot message entry endpoint 
@app.post("/message/", response_model=MessageResponse)
async def message(item: MessageRequest, api_key: APIKey = Depends(get_api_key)):
    logger.info(f"Message received: {item.message}")

    # Send message to assistant
    message = client.beta.threads.messages.create(
        thread_id=item.thread_id,
        role="user",
        content=item.message
    )

    run = client.beta.threads.runs.create(
        thread_id=item.thread_id,
        assistant_id=assistant_id # use the assistant id defined aboe
    )

    run = main_loop(run, item.thread_id)

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(limit=1, thread_id=item.thread_id)
        messages_json = json.loads(messages.model_dump_json())
        message_content = messages_json['data'][0]['content']
        text = message_content[0].get('text', {}).get('value')
        return MessageResponse(message=text)
    else:
        return MessageResponse(message="Assistant reported an error.")


@app.post("/thread/", response_model=ThreadResponse)
async def thread(api_key: APIKey = Depends(get_api_key)):
    thread = client.beta.threads.create()    
    logger.info(f"Thread created with ID: {thread.id}")
    return ThreadResponse(thread_id=thread.id)

# Uvicorn startup
# uvicorn FastAPI:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8324)