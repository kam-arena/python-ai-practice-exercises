import asyncio
import os
from agent_framework import HostedCodeInterpreterTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential, 
                           project_endpoint=os.getenv("AZURE_PROJECT_ENDPOINT"),
                           model_deployment_name=os.getenv("MODEL")).create_agent(
            name="CodingAgent",
            instructions="You are a helpful assistant that can write and execute Python code.",
            tools=HostedCodeInterpreterTool()
        ) as agent,
    ):
        result = await agent.run("Calculate the factorial of 20 using Python code.")
        print(result.text)

asyncio.run(main())