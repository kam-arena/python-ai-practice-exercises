import os
from dotenv import load_dotenv
import asyncio
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from azure.identity import DefaultAzureCredential
from azure.identity.aio import get_bearer_token_provider

# Cargar .env (busca .env en el directorio de trabajo)
load_dotenv()

# Obtener variables de entorno
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL = os.getenv("OPENAI_MODEL") or os.getenv("MODEL")

if not AZURE_OPENAI_ENDPOINT or not MODEL:
    raise RuntimeError("Faltan variables de entorno: AZURE_OPENAI_ENDPOINT y/o OPENAI_MODEL (defínelas en .env)")

client = OpenAIChatClient(
    base_url=AZURE_OPENAI_ENDPOINT.rstrip("/") + "/openai/v1/",
    api_key=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"),
    model_id=MODEL
    )

agent = ChatAgent(chat_client=client, instructions = "You're an informational agent. Answer questions cheerfully.")

async def main():
    response = await agent.run("Whats weather today in San Francisco?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())