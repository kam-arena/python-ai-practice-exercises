import asyncio
import os
from dotenv import load_dotenv
import random
from datetime import datetime
from typing import Annotated
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from azure.identity import DefaultAzureCredential
from azure.identity.aio import get_bearer_token_provider
from pydantic import Field

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL = os.getenv("OPENAI_MODEL") or os.getenv("MODEL")

if not AZURE_OPENAI_ENDPOINT or not MODEL:
    raise RuntimeError(
        "Faltan variables de entorno: AZURE_OPENAI_ENDPOINT y/o OPENAI_MODEL (defínelas en .env)"
    )

client = OpenAIChatClient(
    base_url=AZURE_OPENAI_ENDPOINT.rstrip("/") + "/openai/v1/",
    api_key=get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    ),
    model_id=MODEL,
)

def get_weather(
    city: Annotated[str, Field(description="The city to get the weather for.")],
    date: Annotated[str, Field(description="The date to get weather for in format YYYY-MM-DD.")],
) -> dict:
    print(f"Getting weather for {city} on {date}")
    if random.random() < 0.05:
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

def find_recipes(
    query: Annotated[str, Field(description="User query or desired meal/ingredient")],
) -> list[dict]:
    print(f"Finding recipes for '{query}'")
    if "pasta" in query.lower():
        recipes = [
            {
                "title": "Pasta Primavera",
                "ingredients": ["pasta", "vegetables", "olive oil"],
                "steps": ["Cook pasta.", "Sauté vegetables."],
            }
        ]
    elif "tofu" in query.lower():
        recipes = [
            {
                "title": "Tofu Stir Fry",
                "ingredients": ["tofu", "soy sauce", "vegetables"],
                "steps": ["Cube tofu.", "Stir fry veggies."],
            }
        ]
    else:
        recipes = [
            {
                "title": "Grilled Cheese Sandwich",
                "ingredients": ["bread", "cheese", "butter"],
                "steps": ["Butter bread.", "Place cheese between slices.", "Grill until golden brown."],
            }
        ]
    return recipes

def check_fridge() -> list[str]:
    print("Checking fridge for current ingredients")
    if random.random() < 0.5:
        items = ["pasta", "tomato sauce", "bell peppers", "olive oil"]
    else:
        items = ["tofu", "soy sauce", "broccoli", "carrots"]
    return items

weekend_agent = ChatAgent(
    chat_client=client,
    instructions=("You help users plan their weekends and choose the best activities for the given weather. " "If an activity would be unpleasant in the weather, don't suggest it. " "Include the date of the weekend in your response."),
    tools=[get_weather, get_activities, get_current_date],
)

meal_agent = ChatAgent(
    chat_client=client,
    instructions=(
        "You help users plan meals and choose the best recipes. " "Include the ingredients and cooking instructions in your response. " "Indicate what the user needs to buy from the store when their fridge is missing ingredients."
    ),
    tools=[find_recipes, check_fridge],
)

async def plan_weekend(query: str) -> str:
    print("Tool: plan_weekend invoked")
    response = await weekend_agent.run(query)
    return response.text

async def plan_meal(query: str) -> str:
    print("Tool: plan_meal invoked")
    response = await meal_agent.run(query)
    return response.text

supervisor_agent = ChatAgent(
    chat_client=client,
    instructions=(
        "You are a supervisor managing two specialist agents: a weekend planning agent and a meal planning agent. "
        "Break down the user's request, decide which specialist (or both) to call via the available tools, "
        "and then synthesize a final helpful answer. When invoking a tool, provide clear, concise queries."
    ),
    tools=[plan_weekend, plan_meal],
)

async def main():
    user_query = "What can I do this weekend and what can I cook for lunch?"
    response = await supervisor_agent.run(user_query)
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())