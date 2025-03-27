import pytest
from src.chatbot import Chatbot

def test_basic_chat():
    bot = Chatbot(thread_id="test")
    events = list(bot.stream("Hello"))
    # Expect the response to include a message that echoes the user input or offers assistance.
    response = events[-1]["messages"][-1].content
    assert "Hello" in response or "assist" in response

def test_state_update():
    bot = Chatbot(thread_id="test")
    # Manually update the state.
    bot.update_state({"name": "TestBot", "birthday": "2024-01-01"})
    state = bot.get_state()
    assert state["name"] == "TestBot"
    assert state["birthday"] == "2024-01-01"

def test_state_history():
    bot = Chatbot(thread_id="test")
    list(bot.stream("First message"))
    list(bot.stream("Second message"))
    history = bot.get_state_history()
    assert len(history) >= 2
