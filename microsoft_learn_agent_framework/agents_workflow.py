import asyncio
import os
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack
from typing import Any
from agent_framework import AgentRunUpdateEvent, WorkflowBuilder, WorkflowOutputEvent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

async def create_azure_ai_agent() -> tuple[Callable[..., Awaitable[Any]], Callable[[], Awaitable[None]]]:
    """Helper method to create an Azure AI agent factory and a close function.

    This makes sure the async context managers are properly handled.
    """
    stack = AsyncExitStack()
    cred = await stack.enter_async_context(AzureCliCredential())

    client = await stack.enter_async_context(AzureAIAgentClient(async_credential=cred,
                                                                project_endpoint=os.getenv("AZURE_PROJECT_ENDPOINT"),
                                                                model_deployment_name=os.getenv("MODEL")))

    async def agent(**kwargs: Any) -> Any:
        return await stack.enter_async_context(client.create_agent(**kwargs))

    async def close() -> None:
        await stack.aclose()

    return agent, close

async def main() -> None:
    agent, close = await create_azure_ai_agent()
    try:
        # Create a Writer agent that generates content
        writer = await agent(
            name="Writer",
            instructions=(
                "You are an excellent content writer. You create new content and edit contents based on the feedback."
            ),
        )

        # Create a Reviewer agent that provides feedback
        reviewer = await agent(
            name="Reviewer",
            instructions=(
                "You are an excellent content reviewer. "
                "Provide actionable feedback to the writer about the provided content. "
                "Provide the feedback in the most concise manner possible."
            ),
        )

        # Build the workflow with agents as executors
        workflow = (WorkflowBuilder()
            .set_start_executor(writer)
            .add_edge(writer, reviewer).build())
        
        last_executor_id: str | None = None

        events = workflow.run_stream("Create a slogan for a new electric SUV that is affordable and fun to drive.")
        async for event in events:
            if isinstance(event, AgentRunUpdateEvent):
                # Handle streaming updates from agents
                eid = event.executor_id
                if eid != last_executor_id:
                    if last_executor_id is not None:
                        print()
                    print(f"{eid}:", end=" ", flush=True)
                    last_executor_id = eid
                print(event.data, end="", flush=True)
            elif isinstance(event, WorkflowOutputEvent):
                print("\n===== Final output =====")
                print(event.data)
    finally:
        await close()

if __name__ == "__main__":
    asyncio.run(main())