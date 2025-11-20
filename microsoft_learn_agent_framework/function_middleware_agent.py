import os
import asyncio
from typing import Awaitable, Callable
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import FunctionInvocationContext
from dotenv import load_dotenv

load_dotenv()

def get_time():
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

async def logging_function_middleware(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Awaitable[None]],
) -> None:
    """Middleware that logs function calls."""
    print(f"Calling function: {context.function.name}")

    await next(context)

    print(f"Function result: {context.result}")

async def main():
    credential = AzureCliCredential()

    async with AzureAIAgentClient(async_credential=credential, 
                                  project_endpoint=os.getenv("AZURE_PROJECT_ENDPOINT"),
                                  model_deployment_name=os.getenv("MODEL")).create_agent(
        name="TimeAgent",
        instructions="You can tell the current time.",
        tools=[get_time],
        middleware=[logging_function_middleware],
    ) as agent:
        result = await agent.run("What time is it?")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())