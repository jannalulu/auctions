from .base_agent import BaseAgent
from utils.llm_interface import query_llm

class BuyerAgent(BaseAgent):
    def __init__(self, name, attributes, budget):
        super().__init__(name, attributes)
        self.budget = budget
        self.last_bid = 0

    def act(self, auction_state):
        history = "\n".join(self.conversation_history) if self.conversation_history else "No previous actions"
        prompt = f"""You are {self.name}, a buyer in a common value auction. Your budget is ${self.budget}.
Your previous actions in this auction:
{history}

The current auction state is: {auction_state}
Your goal is to not suffer the winner's curse and overpay. What is your next action? Respond with either 'bid' or 'pass'. Do not say anything else."""
        action = query_llm(prompt)
        current_price = int(auction_state.split("$")[1])
        if action.lower() == "bid" and current_price <= self.budget:
            self.last_bid = current_price
        return action