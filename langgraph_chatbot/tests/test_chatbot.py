import pytest
from langgraph_chatbot.chatbot import Chatbot

def test_basic_chat():
    # Create a Chatbot instance with a test thread id
    bot = Chatbot(thread_id="test")
  
    # Send a simple "Hello" message and collect the event
    events = list(bot.stream("Hello"))
  
    # Get the last message from the bot's response
    response = events[-1]["messages"][-1].content
  
    # Check that the response contains either "Hello" or "assist" to indicate a valid reply.
    assert "Hello" in response or "assist" in response

def test_state_update():
    # Create a Chatbot instance with a test thread id.
    bot = Chatbot(thread_id="test")
  
    # Manually update the state with a name and birthday.
    bot.update_state({"name": "TestBot", "birthday": "2024-01-01"})
  
    # Retrieve the state and check that the values were updated correctly
    state = bot.get_state()
  
    assert state["name"] == "TestBot"
    assert state["birthday"] == "2024-01-01"

def test_state_history():
    # Create a Chatbot instance with a test thread id
    bot = Chatbot(thread_id="test")
  
    # Send a couple of messages to build state history
    list(bot.stream("First message"))
    list(bot.stream("Second message"))
  
    # Get the state history and check that there are at least two checkpoints
    history = bot.get_state_history()
    assert len(history) >= 2
