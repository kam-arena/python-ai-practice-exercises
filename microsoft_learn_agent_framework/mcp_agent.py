from typing import Annotated
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
import os
import anyio

load_dotenv()

def get_specials() -> Annotated[str, "Returns the specials from the menu."]:
    return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """

def get_item_price(
    menu_item: Annotated[str, "The name of the menu item."],
) -> Annotated[str, "Returns the price of the menu item."]:
    return "$9.99"

# Create an agent with tools
agent = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("MODEL"),
).create_agent(
    name="RestaurantAgent",
    description="Answer questions about the menu.",
    tools=[get_specials, get_item_price],
)

# Expose the agent as an MCP server
server = agent.as_mcp_server()

from mcp.server.stdio import stdio_server

async def run():
    async def handle_stdin():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    await handle_stdin()

if __name__ == "__main__":
    anyio.run(run)