from src.chatbot import Chatbot

def main():
    bot = Chatbot()
    print("LangGraph Chatbot")
    print("Type your message to chat with the bot.")
    print("Commands:")
    print("  exit           - Quit the application")
    print("  history        - Show state history checkpoints")
    print("  revert <id>    - Resume execution from a checkpoint (provide the checkpoint_id)")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        elif user_input.lower() == "history":
            history = bot.get_state_history()
            print("State History:")
            for state in history:
                checkpoint = state.config.get("checkpoint_id", "N/A")
                next_node = state.next
                num_messages = len(state.values.get("messages", []))
                print(f"Checkpoint ID: {checkpoint} | Next: {next_node} | Messages: {num_messages}")
        elif user_input.lower().startswith("revert"):
            parts = user_input.split()
            if len(parts) == 2:
                checkpoint_id = parts[1]
                # Update the config with the checkpoint_id for time travel.
                new_config = bot.config.copy()
                new_config["configurable"]["checkpoint_id"] = checkpoint_id
                events = bot.time_travel(new_config)
                for event in events:
                    if "messages" in event:
                        print("Bot:", event["messages"][-1].content)
            else:
                print("Usage: revert <checkpoint_id>")
        else:
            events = bot.stream(user_input)
            for event in events:
                if "messages" in event:
                    print("Bot:", event["messages"][-1].content)

if __name__ == "__main__":
    main()
