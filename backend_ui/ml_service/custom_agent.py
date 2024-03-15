from langchain_openai import ChatOpenAI
from langchain.agents import tool, LocalAgent, OrAgent, WebAgent
from typing import Optional

# Assuming the setup for ChatOpenAI is done correctly elsewhere with the necessary API key
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Example database search tool
@tool
def search_policies_database(question: str) -> Optional[str]:
    """
    Searches the policies database for an answer to the given question.
    Returns a string answer if found, else None.
    """
    # This function should implement the actual search logic against your database
    # For demonstration, let's assume it returns None, indicating no answer found in the database
    return None

# Tool to search over the internet
@tool
def search_internet(question: str) -> Optional[str]:
    """
    Searches the internet for an answer to the given question.
    Returns a string answer if found, else None.
    """
    # Implement web search logic here. This could be a call to a web search API or custom logic
    # For demonstration, let's assume it also returns None for now
    return None

# Local agent to search the policies database
local_agent = LocalAgent(func=search_policies_database)

# Web agent to search over the internet
web_agent = WebAgent(func=search_internet)

# OrAgent to try multiple agents and use the first successful result
agent = OrAgent(agents=[local_agent, web_agent])

@tool
def determine_answer_source(question: str) -> str:
    """
    Determines where the answer to a question can be found.
    Returns a string indicating the source: 'Policies Database', 'Internet', or 'Cannot be answered'.
    """
    result = agent(question)
    if result is None:
        return "Cannot be answered"
    elif result.agent == local_agent:
        return "Policies Database"
    elif result.agent == web_agent:
        return "Internet"

# Example usage
question = "What is the policy on remote work?"
source = determine_answer_source(question)
print(f"The question can be answered by: {source}")
