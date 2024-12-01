from auctions.english_auction import EnglishAuction
from auctions.dutch_auction import DutchAuction
from auctions.common_auction import CommonAuction
from agents.buyer_agent import BuyerAgent
from agents.auctioneer_agent import AuctioneerAgent
import yaml
import argparse

def run_auction(config):
    buyers = [BuyerAgent(f"Buyer_{i}", buyer['attributes'], buyer['budget']) # Pass in buyer attributes from config
      for i, buyer in enumerate(config['buyers'])]
    auctioneer = AuctioneerAgent("Auctioneer", config['auctioneer_attributes'])
    
    # Type of auction that I'm running
    auction = DutchAuction( # auction = EnglishAuction / CommonAuction / DutchAuction
        config['item'],
        config['starting_price'],
        buyers,
        auctioneer,
        config['price_decrement'], #or config['price_decrement'] for Dutch Auctions and _increment for English / Common Auction
        config['log_file']
    )
    
    results = auction.run()
    return results

if __name__ == "__main__":  
  parser = argparse.ArgumentParser()
  parser.add_argument('--loop', action='store_true', help='Run the auction 10 times')
  args = parser.parse_args()
  
  with open('config/config.yaml', 'r') as f:
      config = yaml.safe_load(f)
  
  if args.loop:
    for i in range(11):
      print(f"\nAuction {i+1}/11")
      results = run_auction(config)
      print(results)
  else:
    results = run_auction(config)
    print(results)
