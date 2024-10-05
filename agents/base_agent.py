from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        self.memory = []

    @abstractmethod
    def act(self, auction_state):
        pass

    def update_memory(self, event):
        self.memory.append(event)

    def get_memory(self):
        return self.memory