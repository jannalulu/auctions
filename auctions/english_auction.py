from .base_auction import BaseAuction

class EnglishAuction(BaseAuction):
    def __init__(self, item, starting_price, buyers, auctioneer, increment, log_file):
        super().__init__(item, starting_price, buyers, auctioneer, log_file)
        self.increment = increment
        self.max_rounds = 100
        self.winner = None
        self.starting_price = starting_price

    def run(self):
        self.current_price = self.starting_price
        round_count = 0
        
        while round_count < self.max_rounds:
            auctioneer_action = self.auctioneer.announce_price(self.current_price, self.item)
            self.log_action(self.auctioneer, auctioneer_action)

            active_bidders = 0
            for buyer in self.buyers:
                buyer_action = buyer.act(self.get_auction_state())
                self.log_action(buyer, buyer_action)
                if self.process_buyer_action(buyer, buyer_action):
                    active_bidders += 1
            
            if active_bidders == 0 or active_bidders == 1:
                if round_count == 0:
                    self.log_action(self.auctioneer, "No sale - no bids at starting price")
                else:
                    self.determine_winner()
                    if self.winner:
                        self.log_action(self.auctioneer, f"Sold to {self.winner.name} for ${self.current_price}!")
                break
            
            self.current_price += self.increment
        
        self.close_logger()
        return self.end_auction()

    def process_buyer_action(self, buyer, action):
        if action.lower() == "bid":
            if self.current_price <= buyer.budget:
                buyer.last_bid = self.current_price
                return True
            return False
        return False

    def determine_winner(self):
        highest_bidder = max(self.buyers, key=lambda b: b.last_bid if hasattr(b, 'last_bid') else 0)
        if hasattr(highest_bidder, 'last_bid'):
            self.winner = highest_bidder
            self.final_price = highest_bidder.last_bid
    
    def get_auction_state(self):
        return f"Current price: ${self.current_price}"
        
    def process_seller_action(self, action):
        return True
