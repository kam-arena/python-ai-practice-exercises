import os
import asyncio
from typing import Awaitable, Callable
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import AgentRunContext
from dotenv import load_dotenv

load_dotenv()

async def logging_agent_middleware(
    context: AgentRunContext,
    next: Callable[[AgentRunContext], Awaitable[None]],
) -> None:
    """Simple middleware that logs agent execution."""
    print("Agent starting...")

    # Continue to agent execution
    await next(context)

    print("Agent finished!")

async def main():
    credential = AzureCliCredential()

    async with AzureAIAgentClient(async_credential=credential, 
                                  project_endpoint=os.getenv("AZURE_PROJECT_ENDPOINT"),
                                  model_deployment_name=os.getenv("MODEL")).create_agent(
        name="GreetingAgent",
        instructions="You are a friendly greeting assistant.",
        middleware=logging_agent_middleware,  # Add your middleware here
    ) as agent:
        result = await agent.run("Hello!")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())