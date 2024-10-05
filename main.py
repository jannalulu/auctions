# from auctions.english_auction import EnglishAuction
from auctions.dutch_auction import DutchAuction
from agents.buyer_agent import BuyerAgent
from agents.seller_agent import SellerAgent
from agents.auctioneer_agent import AuctioneerAgent
import yaml

def run_auction(config):
    seller = SellerAgent("Seller", config['seller']['attributes']) # Pass in seller attributes from config
    buyers = [BuyerAgent(f"Buyer_{i}", buyer['attributes'], buyer['budget']) # Pass in buyer attributes from config
      for i, buyer in enumerate(config['buyers'])]
    auctioneer = AuctioneerAgent("Auctioneer", config['auctioneer_attributes'])
    
    # Type of auction that I'm running
    auction = DutchAuction( # auction = EnglishAuction( for English
        config['item'],
        config['starting_price'],
        seller,
        buyers,
        auctioneer,
        config['price_decrement'], #or config['price_increment'] for English Auctions
        config['log_file'],
        config ['max_rounds'] # comment out for English auctions
    )
    
    results = auction.run()
    return results

if __name__ == "__main__":
  with open('config/config.yaml', 'r') as f:
      config = yaml.safe_load(f)
  
  results = run_auction(config)
  print(results)
