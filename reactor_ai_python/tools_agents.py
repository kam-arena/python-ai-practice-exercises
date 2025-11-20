import asyncio
import random
from typing import Annotated
from datetime import datetime
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
    
def get_activities(
    city: Annotated[str, Field(description="The city to get activities for.")],
    date: Annotated[str, Field(description="The date to get activities for in format YYYY-MM-DD.")],
) -> list[dict]:
    print(f"Getting activities for {city} on {date}")
    return [
        {"name": "Hiking", "location": city},
        {"name": "Beach", "location": city},
        {"name": "Museum", "location": city},
    ]

def get_current_date() -> str:
    print("Getting current date")
    return datetime.now().strftime("%Y-%m-%d")
    
agent = ChatAgent(
    chat_client=client, 
    instructions="You help users plan their weekends and choose the best activities for the given weather. " 
                 "If an activity would be unpleasant in weather, don't suggest it. Include date of the weekend in response.", 
    tools=[get_weather, get_activities, get_current_date])

async def main():
    response = await agent.run("hii what can I do this weekend in San Francisco?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())