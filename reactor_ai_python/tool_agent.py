import asyncio
import random
from typing import Annotated
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from azure.identity import DefaultAzureCredential
from azure.identity.aio import get_bearer_token_provider
from pydantic import Field
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

client = OpenAIChatClient(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT") + "/openai/v1/",
    api_key=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"),
    model_id=os.getenv("MODEL")
)

def get_weather(
        city: Annotated[str, Field(description="City name, spelled out fully")],) -> dict:
    print(f"Getting weather for {city}")
    if random.random() < 0.5:
        return {"temperature": 72, "description": "Sunny"}
    else:
        return {"temperature": 60, "description": "Rainy"}
    
agent = ChatAgent(
    chat_client=client, 
    instructions="You're an informational agent. Answer questions cheerfully.", 
    tools=[get_weather])

async def main():
    response = await agent.run("Whats weather today in sf?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())