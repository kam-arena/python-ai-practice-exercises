import asyncio
import os
from dataclasses import dataclass
from pydantic import BaseModel

from agent_framework import (
    AgentExecutor,
    AgentExecutorRequest,
    AgentExecutorResponse,
    ChatMessage,
    Executor,
    RequestInfoEvent,
    Role,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowOutputEvent,
    WorkflowRunState,
    WorkflowStatusEvent,
    handler,
    response_handler,
)
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

@dataclass
class HumanFeedbackRequest:
    """Request message for human feedback in the guessing game."""
    prompt: str = ""
    guess: int | None = None

class GuessOutput(BaseModel):
    """Structured output from the AI agent with response_format enforcement."""
    guess: int

class TurnManager(Executor):
    """Coordinates turns between the AI agent and human player.

    Responsibilities:
    - Start the game by requesting the agent's first guess
    - Process agent responses and request human feedback
    - Handle human feedback and continue the game or finish
    """

    def __init__(self, id: str | None = None):
        super().__init__(id=id or "turn_manager")

    @handler
    async def start(self, _: str, ctx: WorkflowContext[AgentExecutorRequest]) -> None:
        """Start the game by asking the agent for an initial guess."""
        user = ChatMessage(Role.USER, text="Start by making your first guess.")
        await ctx.send_message(AgentExecutorRequest(messages=[user], should_respond=True))

    @handler
    async def on_agent_response(
        self,
        result: AgentExecutorResponse,
        ctx: WorkflowContext,
    ) -> None:
        """Handle the agent's guess and request human guidance."""
        # Parse structured model output (defensive default if agent didn't reply)
        text = result.agent_run_response.text or ""
        last_guess = GuessOutput.model_validate_json(text).guess if text else None

        # Craft a clear human prompt that defines higher/lower relative to agent's guess
        prompt = (
            f"The agent guessed: {last_guess if last_guess is not None else text}. "
            "Type one of: higher (your number is higher than this guess), "
            "lower (your number is lower than this guess), correct, or exit."
        )
        # Send a request using the request_info API
        await ctx.request_info(
            request_data=HumanFeedbackRequest(prompt=prompt, guess=last_guess),
            response_type=str
        )

    @response_handler
    async def on_human_feedback(
        self,
        original_request: HumanFeedbackRequest,
        feedback: str,
        ctx: WorkflowContext[AgentExecutorRequest, str],
    ) -> None:
        """Continue the game or finish based on human feedback."""
        reply = feedback.strip().lower()
        # Use the correlated request's guess to avoid extra state reads
        last_guess = original_request.guess

        if reply == "correct":
            await ctx.yield_output(f"Guessed correctly: {last_guess}")
            return

        # Provide feedback to the agent for the next guess
        user_msg = ChatMessage(
            Role.USER,
            text=f'Feedback: {reply}. Return ONLY a JSON object matching the schema {{"guess": <int 1..10>}}.',
        )
        await ctx.send_message(AgentExecutorRequest(messages=[user_msg], should_respond=True))

async def main() -> None:
    # Create the chat agent with structured output enforcement
    chat_client = AzureOpenAIChatClient(credential=AzureCliCredential(),
                                        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                        deployment_name=os.getenv("MODEL"))
    agent = chat_client.create_agent(
        instructions=(
            "You guess a number between 1 and 10. "
            "If the user says 'higher' or 'lower', adjust your next guess. "
            'You MUST return ONLY a JSON object exactly matching this schema: {"guess": <integer 1..10>}. '
            "No explanations or additional text."
        ),
        response_format=GuessOutput,
    )

    # Create workflow components
    turn_manager = TurnManager(id="turn_manager")
    agent_exec = AgentExecutor(agent=agent, id="agent")

    # Build the workflow graph
    workflow = (
        WorkflowBuilder()
        .set_start_executor(turn_manager)
        .add_edge(turn_manager, agent_exec)  # Ask agent to make/adjust a guess
        .add_edge(agent_exec, turn_manager)  # Agent's response goes back to coordinator
        .build()
    )

    # Execute the interactive workflow
    await run_interactive_workflow(workflow)

async def run_interactive_workflow(workflow):
    """Run the workflow with human-in-the-loop interaction."""
    pending_responses: dict[str, str] | None = None
    completed = False
    workflow_output: str | None = None

    print("🎯 Number Guessing Game")
    print("Think of a number between 1 and 10, and I'll try to guess it!")
    print("-" * 50)

    while not completed:
        # First iteration uses run_stream("start")
        # Subsequent iterations use send_responses_streaming with pending responses
        stream = (
            workflow.send_responses_streaming(pending_responses)
            if pending_responses
            else workflow.run_stream("start")
        )

        # Collect events for this turn
        events = [event async for event in stream]
        pending_responses = None

        # Process events to collect requests and detect completion
        requests: list[tuple[str, str]] = []  # (request_id, prompt)
        for event in events:
            if isinstance(event, RequestInfoEvent) and isinstance(event.data, HumanFeedbackRequest):
                # RequestInfoEvent for our HumanFeedbackRequest
                requests.append((event.request_id, event.data.prompt))
            elif isinstance(event, WorkflowOutputEvent):
                # Capture workflow output when yielded
                workflow_output = str(event.data)
                completed = True

        # Check workflow status
        pending_status = any(
            isinstance(e, WorkflowStatusEvent) and e.state == WorkflowRunState.IN_PROGRESS_PENDING_REQUESTS
            for e in events
        )
        idle_with_requests = any(
            isinstance(e, WorkflowStatusEvent) and e.state == WorkflowRunState.IDLE_WITH_PENDING_REQUESTS
            for e in events
        )

        if pending_status:
            print("🔄 State: IN_PROGRESS_PENDING_REQUESTS (requests outstanding)")
        if idle_with_requests:
            print("⏸️  State: IDLE_WITH_PENDING_REQUESTS (awaiting human input)")

        # Handle human requests if any
        if requests and not completed:
            responses: dict[str, str] = {}
            for req_id, prompt in requests:
                print(f"\n🤖 {prompt}")
                answer = input("👤 Enter higher/lower/correct/exit: ").lower()

                if answer == "exit":
                    print("👋 Exiting...")
                    return
                responses[req_id] = answer
            pending_responses = responses

    # Show final result
    print(f"\n🎉 {workflow_output}")