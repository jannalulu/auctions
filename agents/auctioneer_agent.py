from .base_agent import BaseAgent
from utils.llm_interface import query_llm

class AuctioneerAgent(BaseAgent):
    def __init__(self, name, attributes):
        super().__init__(name, attributes)

    def act(self, auction_state):
        prompt = f"You are {self.name}, an auctioneer. The current auction state is: {auction_state}. What is your next action? Respond with a statement to encourage bidding or close the auction."
        action = query_llm(prompt)
        return action

    def announce_price(self, price, item):
        return f"The current bid is ${price} for {item}. Do I hear any advance on ${price}?"

    def close_auction(self, winner, final_price):
        return f"Sold to {winner} for ${final_price}!"