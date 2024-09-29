import random

class LLMAgent:
    def __init__(self, name, budget, strategy):
        self.name = name
        self.budget = budget
        self.strategy = strategy

    def place_bid(self, current_price, highest_bid):
        if self.strategy == "aggressive":
            max_increase = min(50, self.budget - highest_bid)
            bid = min(highest_bid + random.randint(1, max_increase), self.budget)
        else:  # conservative
            max_increase = min(20, self.budget - highest_bid)
            bid = min(highest_bid + random.randint(1, max_increase), self.budget)
        
        return bid if bid > highest_bid else 0

def run_english_first_price_auction(item, start_price, agents):
    print(f"Starting English first-price auction for {item} at ${start_price}")
    highest_bid = start_price - 1
    winner = None
    round = 0

    while True:
        round += 1
        print(f"\nRound {round}")
        no_new_bids = True

        for agent in agents:
            bid = agent.place_bid(start_price, highest_bid)
            if bid > highest_bid:
                highest_bid = bid
                winner = agent
                print(f"{agent.name} bids ${bid}")
                no_new_bids = False
        
        if no_new_bids:
            break

    if winner:
        print(f"\nAuction ended. {winner.name} wins with a bid of ${highest_bid}")
    else:
        print("\nAuction ended. No winner.")

# Create LLM agents
agent1 = LLMAgent("Agent 1", budget=1000, strategy="aggressive")
agent2 = LLMAgent("Agent 2", budget=1200, strategy="conservative")

# Run the auction
run_english_first_price_auction("Rare Book", start_price=500, agents=[agent1, agent2])