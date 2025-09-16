import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
# Import the agent from the new directory
from account_discovery_agent.agent import root_agent
from google.genai import types as genai_types


async def main():
    """Runs the agent with a sample query."""
    session_service = InMemorySessionService()
    # Define the inputs for our agent in the session state
    initial_state = {
        "url": "https://google.com",
        "selected_prompts": "- Company Overview\n- Products and Services",
        "custom_instructions": "Focus on their AI initiatives."
    }
    await session_service.create_session(
        app_name="account_discovery_agent",
        user_id="test_user",
        session_id="test_session",
        state=initial_state
    )
    runner = Runner(
        agent=root_agent, app_name="account_discovery_agent", session_service=session_service
    )
    # The agent's instruction is parameterized, so the user message can be simple.
    query = "Generate the report."
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=query)]
        ),
    ):
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
