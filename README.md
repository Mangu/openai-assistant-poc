## create_assistant.ipynb

This Jupyter notebook is used to create an assistant using Azure OpenAI's API. It cleates a new assistant each time is it ran. It prints the created asistant id which you will use in the test_assistant notebook

It might be a good idea to creat a third notebook that modifies an assistant given an ID.

## test_assistant.ipynb

This is a test harness for the assistant. Make sure you have the right assitant id in the second cell of the notebook.

## FastAPI.py

This creates REST api for the given assistant. The assistant id is configured on line 18. It uses the "Fast" framework.

It creates two api \thread and \message. Thread must be called first to innitiate a thread (sesions). Message allows you to send a question to the assistant and returns the answers from the assistant.

Sample paid loads are available in the test_api.http file.

To run locally type `# uvicorn rest_api:app --reload` in a command prompt.

## test_api

It uses the VS Code extension "REST Client". Once the extention is install you will see a `Send Request` link on top of each "verb"

## account.py, cmdb.py, crs.py, logs.py

These fuctions provides the assitant with all the data it needs to answer questions. If changes are made to the "signature" of these functions, the appropiate changes need to be made to the assistant to it can understand how to use / call them

## running with copilot studio

if you are running the REST APIs locally, copilot studio can't reach them. To get around this, I used "serveo.net". Serveo is an SSH server just for remote port forwarding. When a user connects to Serveo, they get a public URL that anybody can use to connect to their localhost server.

I open the port transfering by running `ssh -R 80:127.0.0.1:8000 serveo.net` in a command prompt. Make sure to change the ip or host accordingly.

ssh -R 80:127.0.0.1:8000 serveo.net

## sample questions

- What is the application, jvm, host and Port of the affected system whose Port_Name is INDY46 ?

- For Applications whose Port_Name is INDY46, is the host a sox system?
- For Applications whose Port_Name is INDY46, what are the logs of the affected systems?

- Are there any CRS for the affected system whose application Port_Name is INDY46 ?

## links

- [Getting started with Azure OpenAI Assistants](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/assistant)

- [Assistant API docs](https://platform.openai.com/docs/api-reference/assistants)