from langgraph_chatbot.chatbot import Chatbot

def main():
    # Initialize our Chatbot instance with a default thread id "1"
    bot = Chatbot()
    print("Welcome to the Chatbot!")
    print("You can chat with the bot, view state history, or revert to a previous checkpoint.")
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
            # Get and display the state history for time travel debugging
            history = bot.get_state_history()
            print("State History:")
          
            for state in history:
                # Each state has a checkpoint_id (if available), next node info, and number of messages stored
                checkpoint = state.config.get("checkpoint_id", "N/A")
                next_node = state.next
                num_messages = len(state.values.get("messages", []))
              
                print(f"Checkpoint ID: {checkpoint} | Next: {next_node} | Messages: {num_messages}")
        
        elif user_input.lower().startswith("revert"):
            # Revert to a specific checkpoint based on user-provided checkpoint id
            parts = user_input.split()
          
            if len(parts) == 2:
                checkpoint_id = parts[1]
                # Copy current config and add checkpoint_id for time travel
                new_config = bot.config.copy()
                new_config["configurable"]["checkpoint_id"] = checkpoint_id
                events = bot.time_travel(new_config)
              
                for event in events:
                    if "messages" in event:
                        print("Bot:", event["messages"][-1].content)
            else:
                print("Usage: revert <checkpoint_id>")
              
        else:
            # Normal chat message: send user input to the chatbot
            events = bot.stream(user_input)
            for event in events:
                if "messages" in event:
                    # Print the latest message content from the bot
                    print("Bot:", event["messages"][-1].content)

if __name__ == "__main__":
    main()
