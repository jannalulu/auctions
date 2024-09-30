import random
from dataclasses import dataclass

@dataclass
class Bid:
    amount: int
    bidder: 'Agent'

class Agent:
    def __init__(self, name: str, budget: int, target_price: int):
        self.name = name
        self.budget = budget
        self.target_price = target_price

    def decide_to_bid(self, current_price: int) -> bool:
        return current_price <= min(self.budget, self.target_price)

class DutchAuction:
    def __init__(self, item: str, start_price: int, min_price: int, price_decrement: int):
        self.item = item
        self.start_price = start_price
        self.min_price = min_price
        self.price_decrement = price_decrement
        self.current_price = start_price
        self.winner: Agent | None = None
        self.round = 0

    def run(self, agents: list[Agent]):
        print(f"Starting Dutch auction for {self.item} at ${self.start_price}")

        while self.current_price >= self.min_price:
            self.round += 1
            print(f"\nRound {self.round}: Current price ${self.current_price}")

            if self._check_bids(agents):
                break

            self.current_price -= self.price_decrement

        self._announce_result()

    def _check_bids(self, agents: list[Agent]) -> bool:
        for agent in agents:
            if agent.decide_to_bid(self.current_price):
                self.winner = agent
                return True
        return False

    def _announce_result(self):
        if self.winner:
            print(f"\nAuction ended. {self.winner.name} wins with a bid of ${self.current_price}")
        else:
            print(f"\nAuction ended. No winner. Item not sold. Final price: ${self.current_price}")

def main():
    agent1 = Agent("Agent 1", budget=1000, target_price=1000)
    agent2 = Agent("Agent 2", budget=1200, target_price=1200)
    
    auction = DutchAuction("Rare Painting", start_price=1500, min_price=500, price_decrement=50)
    auction.run([agent1, agent2])

if __name__ == "__main__":
    main()