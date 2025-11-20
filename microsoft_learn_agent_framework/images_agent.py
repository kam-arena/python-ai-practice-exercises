import asyncio
from agent_framework import ChatMessage, TextContent, DataContent, Role
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

agent = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("MODEL"),
).create_agent(
    name="VisionAgent",
    instructions="Eres un agente útil que puede analizar imágenes",
)

script_dir = Path(__file__).parent
img_path = script_dir / "images" / "Goku.jpg"

# Load image from local file
with open(img_path, "rb") as f:
    image_bytes = f.read()

message = ChatMessage(
    role=Role.USER,
    contents=[
        TextContent(text="¿Qué ves en esta imagen?"),
        DataContent(
            data=image_bytes,
            media_type="image/jpeg"
        )
    ]
)

# Send message to agent and get response
response = asyncio.run(agent.run(message))
print(response.text)