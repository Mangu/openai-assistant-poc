# Overview

This repository showcases the power of the Azure OpenAI Assistant API by providing a robust implementation of a cutting-edge AI agent. Our goal is to help you accelerate the creation of a compelling proof of concept that demonstrates the immense value of AI solutions. With this solid foundation, you can seamlessly transition to a pilot or even a minimum viable product, ensuring a smooth path towards success.

## Getting Started with Azure OpenAI Assistant

For more information, refer to the documentation and resources below:

- [Azure OpenAI Assistants API Reference](https://platform.openai.com/docs/api-reference/assistants)
- [Azure OpenAI Assistants Getting Started Guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/assistant)

## Helper Notebooks

### create_assistant.ipynb

This Jupyter notebook demonstrates how to create an assistant using Azure OpenAI's API. Each time it is run, a new assistant is created and its ID is printed. You can use this ID in the test_assistant notebook.

Additionally, this notebook includes instructions on how to modify the code to switch from creating a new assistant to updating an existing one. This  allows you to easily adapt the assistant to your evolving needs.

By following the steps outlined in this notebook, you can quickly create or modify an Azure OpenAI Assistants whithout gaving to go to the portal.

### test_assistant.ipynb

This is a test harness for the assistant. Make sure you have the correct assistant ID in the second cell of the notebook. It allows you to test the assistant configuration right from a notebook.

### rest_api.py

This is the REST API for the assistant which uses the "Fast" framework and the asistant APIs. The assistant ID is configured on line 18 of the code.

The API consists of two endpoints: `/thread` and `/message`. The `/thread` endpoint should be called first to initiate a thread (session) with the assistant. Once the thread is established, you can use the `/message` endpoint to send questions to the assistant and receive answers in response.

For more information on FastAPI please go to: [FastAPI Documentation](https://fastapi.tiangolo.com/)

To test the API, you can use the sample payloads provided in the `test_api.http` file.

To run the API locally, open a command prompt and type `uvicorn rest_api:app --reload`.

### test_api.http

It uses the VS Code extension "REST Client". Once the extention is installed you will see a `Send Request` link on top of each "verb"


### Running locally

If you are running the REST APIs locally for development, but need to expose it to the cloud like Copilot Studio, the API can't be reached. To get around this, you can use "serveo.net". Serveo is an SSH server just for remote port forwarding. When a user connects to Serveo, they get a public URL that anybody can use to connect to their localhost server.

You can open the port transferring by running `ssh -R 80:127.0.0.1:8000 serveo.net` in a command prompt. Make sure to change the IP or host accordingly.

ssh -R 80:127.0.0.1:8000 serveo.net

### Sample Questions

