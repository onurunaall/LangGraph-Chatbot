# LangGraph Chatbot

This is a support chatbot project built with LangGraph. It is designed as a learning project to demonstrate several key features:
  
- **State Management & Custom State:** We use a LangGraph `StateGraph` with custom keys (like `messages`, `name`, and `birthday`).
- **Tool Integration:** The chatbot integrates external tools (a simulated web search tool and a human assistance tool).
- **Memory & Checkpointing:** It saves conversation state using an in-memory checkpointer.
- **Human-in-the-Loop:** It can pause and request human input when needed.
- **Time Travel:** You can revert to previous checkpoints (like rewinding a conversation).
