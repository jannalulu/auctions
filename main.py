# from auctions.english_auction import EnglishAuction
# from auctions.dutch_auction import DutchAuction
from auctions.common_auction import CommonAuction
from agents.buyer_agent import BuyerAgent

from agents.auctioneer_agent import AuctioneerAgent
import yaml

def run_auction(config):
    buyers = [BuyerAgent(f"Buyer_{i}", buyer['attributes'], buyer['budget']) # Pass in buyer attributes from config
      for i, buyer in enumerate(config['buyers'])]
    auctioneer = AuctioneerAgent("Auctioneer", config['auctioneer_attributes'])
    
    # Type of auction that I'm running
    auction = CommonAuction( # auction = EnglishAuction( for English
        config['item'],
        config['starting_price'],
        buyers,
        auctioneer,
        config['price_increment'], #or config['price_decrement'] for Dutch Auctions
        config['log_file'],
        # config ['max_rounds'] # comment out for English and common auctions
    )
    
    results = auction.run()
    return results

if __name__ == "__main__":
  with open('config/config.yaml', 'r') as f:
      config = yaml.safe_load(f)
  
  results = run_auction(config)
  print(results)
