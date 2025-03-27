from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.types import interrupt

@tool
def human_assistance(query: str) -> str:
    """
    This tool simulates human assistance.
    It prints the query and then prompts the user to type a response.
    """
  
    print(f"[Human Assistance] Query: {query}")
  
    # Simulate waiting for human input with the input() function.
    response = input("Enter human assistance response: ")
  
    return response

def get_search_tool():
    """
    Returns an instance of the Tavily search tool.
    This tool simulates a web search by returning dummy results.
    """
    return TavilySearchResults(max_results=2)

