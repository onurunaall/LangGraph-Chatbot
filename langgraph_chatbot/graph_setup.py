from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command

from langchain_anthropic import ChatAnthropic
from langgraph_chatbot.tools import get_search_tool, human_assistance

class State(TypedDict):
    messages: Annotated[list, add_messages] # This holds the conversation messages
    name: str # A custom key to store a name
    birthday: str # A custom key to store a birthday

def build_graph():
    """
    Build and compile the LangGraph state graph.
    This function creates nodes, sets up edges, and returns the compiled graph.
    """
    graph_builder = StateGraph(State)
    
    # Initialize tools
    search_tool = get_search_tool()
    tools = [search_tool, human_assistance]

    # Initialize the LLM (here using Anthropic's Claude model) and bind our tools to it.
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    llm_with_tools = llm.bind_tools(tools)

    # Define the chatbot node.
    # This function takes the current state, sends the conversation history to the LLM, and returns a new message.
    def chatbot(state: State):
        # Call the LLM with the current messages
        message = llm_with_tools.invoke(state["messages"])
      
        # Check that we don't have more than one tool call per invocation.
        assert len(getattr(message, "tool_calls", [])) <= 1
      
        return {"messages": [message]}
    
    # Add the chatbot node to the graph
    graph_builder.add_node("chatbot", chatbot)

    # Add a tool node using the prebuilt ToolNode from LangGraph
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    # If the chatbot node returns a message with tool calls, route to the "tools" node
    graph_builder.add_conditional_edges("chatbot", tools_condition)
  
    # After executing a tool, route back to the chatbot to continue processing
    graph_builder.add_edge("tools", "chatbot")
  
    # Set the start edge to the chatbot node
    graph_builder.add_edge(START, "chatbot")
    
    # Create an in-memory checkpointer to store conversation states.
    memory = MemorySaver()
  
    # Compile the graph with the checkpointer
    graph = graph_builder.compile(checkpointer=memory)
    return graph
