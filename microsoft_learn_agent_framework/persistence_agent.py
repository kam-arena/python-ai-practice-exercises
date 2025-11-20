import os
import asyncio
import json
import tempfile
from azure.identity import AzureCliCredential
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from dotenv import load_dotenv

load_dotenv()

agent = ChatAgent(
    chat_client=AzureOpenAIChatClient(
        credential=AzureCliCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("MODEL")
    ),
    name="Assistant",
    instructions="You are a helpful assistant."
)

thread = agent.get_new_thread()

async def main():
    # Run the agent and append the exchange to the thread
    response = await agent.run("Tell me a short pirate joke.", thread=thread)
    print(response.text)

    # Serialize the thread state
    serialized_thread = await thread.serialize()
    serialized_json = json.dumps(serialized_thread)

    # Example: save to a local file (replace with DB or blob storage in production)
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "agent_thread.json")
    print(f"Saving thread state to {file_path}")
    with open(file_path, "w") as f:
        f.write(serialized_json)

    # Read persisted JSON
    with open(file_path, "r") as f:
        loaded_json = f.read()

    reloaded_data = json.loads(loaded_json)

    # Deserialize the thread into an AgentThread tied to the same agent type
    resumed_thread = await agent.deserialize_thread(reloaded_data)

    # Continue the conversation with resumed thread
    response = await agent.run("Now tell that joke in the voice of a pirate.", thread=resumed_thread)
    print(response.text)

# Run the async main function
asyncio.run(main())



