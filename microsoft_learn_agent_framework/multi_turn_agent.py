import asyncio
from agent_framework import ChatMessage, TextContent, Role
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
import os

load_dotenv()

agent = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("MODEL")
).create_agent(
    name="MultiturnAgent",
    instructions="Eres un agente útil que cuenta buenos chistes",
)

thread = agent.get_new_thread();

# Bucle de conversación con el agente hasta que se escriba "salir"
while True:
    user_input = input("Tú: ")
    if user_input.lower() == "salir":
        print("Terminando la conversación.")
        break

    response = asyncio.run(agent.run(
        ChatMessage(
            role=Role.USER,
            contents=[TextContent(text=user_input)]
        ),
        thread=thread
    ))
    print("Agente:", response.text)