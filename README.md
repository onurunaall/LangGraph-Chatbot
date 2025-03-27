# LangGraph Chatbot

This project is an advanced support chatbot built with LangGraph. It demonstrates:

- **State Management & Custom State:** Using a LangGraph `StateGraph` with custom keys (e.g. `messages`, `name`, `birthday`).
- **Tool Integration:** Integrating external tools (a simulated web search via Tavily and human assistance via an interrupt).
- **Memory & Checkpointing:** Persistent conversation state using an in-memory checkpointer.
- **Human-in-the-Loop:** Pausing execution to request human input for guidance.
- **Time Travel:** Reverting to previous checkpoints to resume execution from an earlier state.
