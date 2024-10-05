from .base_agent import BaseAgent
from utils.llm_interface import query_llm

class SellerAgent(BaseAgent):
    def __init__(self, name, attributes):
        super().__init__(name, attributes)

    def act(self, auction_state):
        prompt = f"You are {self.name}, a seller in an auction. Your reserve price is ${self.reserve_price}. The current auction state is: {auction_state}. What is your next action? Respond with either 'accept' or 'reject'."
        action = query_llm(prompt)
        return action