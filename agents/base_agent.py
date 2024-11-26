from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        self.memory = []
        self.conversation_history = []

    @abstractmethod
    def act(self, auction_state):
        pass

    def update_memory(self, event):
        self.memory.append(event)

    def get_memory(self):
        return self.memory

    def add_to_history(self, message):
        self.conversation_history.append(message)

    def get_conversation_history(self):
        return self.conversation_history