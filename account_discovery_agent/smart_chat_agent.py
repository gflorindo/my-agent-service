
from google.adk.agents import Agent
from typing import Optional

from common.config import config


def create_smart_chat_agent(role: str = "Key Account Executive") -> Agent:
    """
    Creates a smart chat agent that can take on different roles.

    Args:
        role: The role for the agent to play (e.g., "Key Account Executive").

    Returns:
        An Agent instance configured to act as a strategic advisor.
    """

    # Define the internal agent for retrieving account data
    internal_agent = Agent(
        name="internal_data_retriever",
        model=config.worker_model,
        instruction="You are an internal agent that retrieves account data from our CRM.",
        description="Retrieves internal account data from the CRM.",
    )

    # Define the external agent for retrieving market news
    external_agent = Agent(
        name="external_news_agent",
        model=config.worker_model,
        instruction="You are an external agent that finds recent market news about a company.",
        description="Finds recent market news and financial data about a company.",
    )

    # Define the coordinator agent
    coordinator_agent = Agent(
        name="strategic_advisor",
        model=config.critic_model,
        instruction=f"You are an experienced {role} and a strategic advisor for the account. "
                    "Your role is to use the available agents to answer questions about the account, "
                    "synthesize the information, and provide strategic advice.",
        description="A smart chat agent that acts as a strategic advisor.",
        sub_agents=[internal_agent, external_agent],
    )

    return coordinator_agent

if __name__ == "__main__":
    # Example of how to create and use the agent
    # This part is for demonstration and can be removed or modified
    from google.adk.runners import Runner
    from google.adk.sessions import Session
    import asyncio

    async def run_agent():
        # Create the agent with a specific role
        smart_agent = create_smart_chat_agent(role="AI Platform Specialist")

        # Create a new session
        session = Session()

        # Create a runner
        runner = Runner(agent=smart_agent)

        # Run the agent with a sample query
        query = "What's the latest news on the account 'TechCorp' and what's their current CRM status?"
        async for event in runner.run_async(session=session, new_message=query):
            if event.is_final_response():
                print(event.content.parts[0].text)

    # Run the async function
    asyncio.run(run_agent())
