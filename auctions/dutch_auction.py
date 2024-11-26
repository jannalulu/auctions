from .base_auction import BaseAuction

class DutchAuction(BaseAuction):
    def __init__(self, item, starting_price, seller, buyers, auctioneer, decrement, logger_filename, max_rounds):
        super().__init__(item, starting_price, seller, buyers, auctioneer, logger_filename)
        self.decrement = decrement
        self.max_rounds = max_rounds
        self.winner = None
        self.starting_price = starting_price  # Add this line to set the starting_price attribute

    def run(self):
        self.current_price = self.starting_price
        round_count = 0
        
        while round_count < self.max_rounds and self.current_price > 0:
            auctioneer_action = self.auctioneer.announce_price(self.current_price)
            self.log_action(self.auctioneer, auctioneer_action)

            for buyer in self.buyers:
                buyer_action = buyer.act(self.get_auction_state())
                self.log_action(buyer, buyer_action)
                auctioneer_response = self.process_buyer_action(buyer, buyer_action)
                self.log_action(self.auctioneer, auctioneer_response)
                
                if buyer_action == "bid":
                    self.winner = buyer
                    self.log_action(self.auctioneer, f"Sold to {self.winner.name} for ${self.current_price}!")
                    self.close_logger()
                    return self.end_auction()
            
            self.current_price -= self.decrement
            round_count += 1
        
        if round_count >= self.max_rounds:
            self.log_action(self.auctioneer, f"Maximum rounds ({self.max_rounds}) reached. Auction ended.")
        else:
            self.log_action(self.auctioneer, f"Price reached zero. Auction ended.")
        self.close_logger()
        return self.end_auction()

    def process_buyer_action(self, buyer, action):
        if action == "bid":
            buyer.last_bid = self.current_price
            return f"Accepted bid from {buyer.name} at ${self.current_price}"
        else:
            return f"{buyer.name} passed"
        
    def process_seller_action(self, action):
        return True
    
    def end_auction(self):
        if self.winner:
            return {
                "winner": self.winner.name,
                "final_price": self.current_price
            }
        else:
            return {
                "winner": None,
                "final_price": None,
                "result": "No sale"
            }

    def get_auction_state(self):
        return f"Current price: ${self.current_price}"