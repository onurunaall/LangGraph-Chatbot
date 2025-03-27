from src.graph_setup import build_graph

class Chatbot:
    def __init__(self, thread_id="1"):
        self.graph = build_graph()
        self.config = {"configurable": {"thread_id": thread_id}}
    
    def stream(self, user_input=None):
        """
        Invoke the graph. If user_input is provided, it creates an initial message.
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
        """
        return self.graph.get_state(self.config)
    
    def get_state_history(self):
        """
        Retrieve the history of states (for time travel purposes).
        """
        return self.graph.get_state_history(self.config)
    
    def update_state(self, update_dict):
        """
        Manually update the state.
        """
        return self.graph.update_state(self.config, update_dict)
    
    def time_travel(self, checkpoint_config):
        """
        Resume execution from a given checkpoint (time travel).
        """
        events = self.graph.stream(None, checkpoint_config, stream_mode="values")
        return events
