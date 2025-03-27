from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.types import interrupt

@tool
def human_assistance(query: str) -> str:
    """
    Request assistance from a human. This simulates an interrupt by prompting for input.
    """
    print(f"[Human Assistance] Query: {query}")
    # Simulate human assistance via input (in production, this would use an interrupt mechanism)
    response = input("Enter human assistance response: ")
    return response

def get_search_tool():
    """
    Returns an instance of the Tavily search tool.
    """
    return TavilySearchResults(max_results=2)
