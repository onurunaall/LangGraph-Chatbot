from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command

from langchain_anthropic import ChatAnthropic
from src.tools import get_search_tool, human_assistance

# Define the state schema with custom keys.
class State(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    birthday: str

def build_graph():
    graph_builder = StateGraph(State)
    
    # Initialize tools.
    search_tool = get_search_tool()
    tools = [search_tool, human_assistance]

    # Initialize the LLM and bind the tools.
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    llm_with_tools = llm.bind_tools(tools)

    # Define the chatbot node.
    def chatbot(state: State):
        # Invoke the LLM with the current message history.
        message = llm_with_tools.invoke(state["messages"])
        # Ensure only one tool call is made per invocation.
        assert len(getattr(message, "tool_calls", [])) <= 1
        return {"messages": [message]}
    
    graph_builder.add_node("chatbot", chatbot)

    # Add a tool node using LangGraph's prebuilt ToolNode.
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    # Conditional routing: if the chatbot's response includes tool calls, go to "tools".
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    # Route back to the chatbot after tool execution.
    graph_builder.add_edge("tools", "chatbot")
    # Start execution at the chatbot node.
    graph_builder.add_edge(START, "chatbot")
    
    # Create an in-memory checkpointer for persistence.
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    return graph
