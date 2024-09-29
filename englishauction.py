import random
from dataclasses import dataclass

@dataclass
class Bid:
    amount: int
    bidder: 'Agent'

class Agent:
    def __init__(self, name: str, budget: int, bid_increase: int):
        self.name = name
        self.budget = budget
        self.bid_increase = bid_increase

    def place_bid(self, current_price: int, is_highest_bidder: bool) -> int:
        if is_highest_bidder or current_price >= self.budget:
            return 0
        
        max_bid = min(current_price + self.bid_increase, self.budget)
        return random.randint(current_price + 1, max_bid)

class Auction:
    def __init__(self, item: str, start_price: int):
        self.item = item
        self.start_price = start_price
        self.current_price = start_price - 1
        self.highest_bid: Bid | None = None
        self.round = 0

    def run(self, agents: list[Agent]):
        print(f"Starting English first-price auction for {self.item} at ${self.start_price}")

        while len(agents) > 1:
            self.round += 1
            print(f"\nRound {self.round}")

            new_highest_bid = self._collect_bids(agents)
            if new_highest_bid == self.highest_bid:
                break

            self.highest_bid = new_highest_bid
            self.current_price = new_highest_bid.amount
            agents = [agent for agent in agents if agent.budget > self.current_price]

        self._announce_result()

    def _collect_bids(self, agents: list[Agent]) -> Bid:
        highest_bid = self.highest_bid or Bid(self.current_price, None)
        
        for agent in agents:
            is_highest_bidder = (agent == self.highest_bid.bidder if self.highest_bid else False)
            bid_amount = agent.place_bid(self.current_price, is_highest_bidder)
            
            if bid_amount > highest_bid.amount:
                highest_bid = Bid(bid_amount, agent)
                print(f"{agent.name} bids ${bid_amount}")

        return highest_bid

    def _announce_result(self):
        if self.highest_bid and self.highest_bid.bidder:
            print(f"\nAuction ended. {self.highest_bid.bidder.name} wins with a bid of ${self.highest_bid.amount}")
        else:
            print("\nAuction ended. No winner.")

def main():
    agent1 = Agent("Agent 1", budget=1000, bid_increase=50)
    agent2 = Agent("Agent 2", budget=1200, bid_increase=30)
    
    auction = Auction("Rare Book", start_price=500)
    auction.run([agent1, agent2])

if __name__ == "__main__":
    main()