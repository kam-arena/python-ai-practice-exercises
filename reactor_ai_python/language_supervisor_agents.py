import asyncio
import os
import random
from dotenv import load_dotenv
from typing import Annotated
from pydantic import Field
from typing import Annotated
from datetime import datetime
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from azure.identity import DefaultAzureCredential
from azure.identity.aio import get_bearer_token_provider

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
    city: Annotated[str, Field(description="Die Stadt, für die das Wetter abgerufen werden soll.")],
    date: Annotated[str, Field(description="Das Datum für die Wettervorhersage im Format YYYY-MM-DD.")],
) -> dict:
    print(f"Hole Wetter für {city} am {date}")
    if random.random() < 0.05:
        return {"Temperatur": 72, "Beschreibung": "Sonnig"}
    else:
        return {"Temperatur": 60, "Beschreibung": "Regnerisch"}

def get_activities(
    city: Annotated[str, Field(description="Die Stadt, für die Aktivitäten gesucht werden.")],
    date: Annotated[str, Field(description="Das Datum für die Aktivitäten im Format YYYY-MM-DD.")],
) -> list[dict]:
    print(f"Hole Aktivitäten für {city} am {date}")
    return [
        {"name": "Wandern", "Standort": city},
        {"name": "Strand", "Standort": city},
        {"name": "Museum", "Standort": city},
    ]

def get_current_date() -> str:
    print("Hole aktuelles Datum")
    return datetime.now().strftime("%Y-%m-%d")

def find_recipes(
    query: Annotated[str, Field(description="Benutzeranfrage oder gewünschte Mahlzeit/Zutat")],
) -> list[dict]:
    print(f"Suche Rezepte für '{query}'")
    if "pasta" in query.lower():
        recipes = [
            {
                "Titel": "Pasta Primavera",
                "Zutaten": ["Nudeln", "Gemüse", "Olivenöl"],
                "Schritte": ["Nudeln kochen.", "Gemüse anbraten."],
            }
        ]
    elif "tofu" in query.lower():
        recipes = [
            {
                "Titel": "Tofu Pfannengericht",
                "Zutaten": ["Tofu", "Sojasauce", "Gemüse"],
                "Schritte": ["Tofu würfeln.", "Gemüse anbraten."],
            }
        ]
    else:
        recipes = [
            {
                "Titel": "Gegrilltes Käsesandwich",
                "Zutaten": ["Brot", "Käse", "Butter"],
                "Schritte": ["Brot buttern.", "Käse zwischen die Scheiben legen.", "Golden braun grillen."],
            }
        ]
    return recipes

def check_fridge() -> list[str]:
    print("Überprüfe Kühlschrank auf vorhandene Zutaten")
    if random.random() < 0.5:
        items = ["Nudeln", "Tomatensauce", "Paprika", "Olivenöl"]
    else:
        items = ["Tofu", "Sojasauce", "Brokkoli", "Karotten"]
    return items

weekend_agent = ChatAgent(
    chat_client=client,
    instructions=("Sie helfen Benutzern bei der Planung ihrer Wochenenden und der Auswahl der besten Aktivitäten für das jeweilige Wetter. " 
                 "Wenn eine Aktivität bei dem Wetter unangenehm wäre, schlagen Sie sie nicht vor. " 
                 "Fügen Sie das Datum des Wochenendes in Ihrer Antwort ein."),
    tools=[get_weather, get_activities, get_current_date],
)

meal_agent = ChatAgent(
    chat_client=client,
    instructions=(
        "Sie helfen Benutzern bei der Planung von Mahlzeiten und der Auswahl der besten Rezepte. " 
        "Fügen Sie die Zutaten und Kochanweisungen in Ihre Antwort ein. " 
        "Geben Sie an, was der Benutzer im Geschäft kaufen muss, wenn Zutaten im Kühlschrank fehlen."
    ),
    tools=[find_recipes, check_fridge],
)

async def plan_weekend(query: str) -> str:
    print("Tool: Wochenendplanung aufgerufen")
    response = await weekend_agent.run(query)
    return response.text

async def plan_meal(query: str) -> str:
    print("Tool: Mahlzeitplanung aufgerufen")
    response = await meal_agent.run(query)
    return response.text

supervisor_agent = ChatAgent(
    chat_client=client,
    instructions=(
        "Sie sind ein Supervisor, der zwei Spezialagenten verwaltet: einen Wochenendplanungsagenten und einen Mahlzeitplanungsagenten. "
        "Analysieren Sie die Anfrage des Benutzers, entscheiden Sie, welchen Spezialisten (oder beide) Sie über die verfügbaren Tools aufrufen möchten, "
        "und erstellen Sie dann eine hilfreiche Endantwort. Verwenden Sie bei der Verwendung eines Tools klare, präzise Anfragen."
    ),
    tools=[plan_weekend, plan_meal],
)

async def main():
    user_query = "Was kann ich dieses Wochenende unternehmen und was kann ich zum Mittagessen kochen?"
    response = await supervisor_agent.run(user_query)
    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())