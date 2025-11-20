import asyncio
from typing import Annotated
from pydantic import Field
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."


openai_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("MODEL"),
)

weather_agent = openai_client.create_agent(
    name="WeatherAgent",
    description="An agent that answers questions about the weather.",
    instructions="You answer questions about the weather.",
    tools=get_weather
)

main_agent = openai_client.create_agent(
    instructions="You are a helpful assistant who responds in French.",
    tools=weather_agent.as_tool()
)

async def main():
    result = await main_agent.run("What is the weather like in Amsterdam?")
    print(result.text)

asyncio.run(main())