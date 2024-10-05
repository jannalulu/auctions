from .base_agent import BaseAgent
from utils.llm_interface import query_llm

class SellerAgent(BaseAgent):
    def __init__(self, name, attributes):
        super().__init__(name, attributes)

    def act(self, auction_state):
        return "accept"