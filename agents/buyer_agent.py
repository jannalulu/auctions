from .base_agent import BaseAgent
from utils.llm_interface import query_anthropic
from utils.llm_interface import query_gemini

class BuyerAgent(BaseAgent):
    def __init__(self, name, attributes, budget):
        super().__init__(name, attributes)
        self.budget = budget
        self.last_bid = 0

    def act(self, auction_state):
        history = "\n".join(self.conversation_history) if self.conversation_history else "No previous actions"
        prompt = f"""
            You are {self.name}, a Pokemon card collector in an all-pay auction. Your budget is ${self.budget}.
            Your previous actions in this auction:
            {history}

            The current auction state is: {auction_state}
            Be careful of winner's curse. What is your next action? If you passed, you cannot bid again. Respond with either 'bid' or 'pass'. Do not say anything else.
        """
        action = query_gemini(prompt).strip()
        current_price = int(auction_state.split("$")[1])
        if action.lower() == "bid" and current_price <= self.budget:
            self.last_bid = current_price
        return action