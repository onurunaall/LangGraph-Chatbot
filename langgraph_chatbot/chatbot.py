from langgraph_chatbot.graph_setup import build_graph

class Chatbot:
    def __init__(self, thread_id="1"):
        # Build the LangGraph graph using our helper function
        self.graph = build_graph()
      
        # Configuration dictionary that holds info like thread_id
        self.config = {"configurable": {"thread_id": thread_id}}
    
    def stream(self, user_input=None):
        """
        This function invokes the graph. If user_input is provided, it creates an initial state
        with the user's message. If not, it resumes the graph without new input.
        """
        if user_input is not None:
            initial_state = {
                "messages": [{"role": "user", "content": user_input}],
                "name": "",
                "birthday": ""
            }
          
            events = self.graph.stream(initial_state, self.config, stream_mode="values")
          
        else:
            events = self.graph.stream(None, self.config, stream_mode="values")
          
        return events

    def get_state(self):
        """
        Retrieve the current state from the graph.
        This is useful to see what the chatbot remembers.
        """
        return self.graph.get_state(self.config)
    
    def get_state_history(self):
        """
        Retrieve the history of states (for time travel purposes).
        This can help you debug or revert the conversation to an earlier point.
        """
        return self.graph.get_state_history(self.config)
    
    def update_state(self, update_dict):
        """
        Manually update the state. For example, you might want to change the name or birthday.
        """
        return self.graph.update_state(self.config, update_dict)
    
    def time_travel(self, checkpoint_config):
        """
        Resume execution from a given checkpoint.
        Use this if you want to "rewind" the conversation.
        """
        events = self.graph.stream(None, checkpoint_config, stream_mode="values")
        return events
