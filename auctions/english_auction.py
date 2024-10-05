from .base_auction import BaseAuction

class EnglishAuction(BaseAuction):
    def __init__(self, item, starting_price, seller, buyers, auctioneer, increment, logger_filename):
        super().__init__(item, starting_price, seller, buyers, auctioneer, logger_filename)
        self.increment = increment
        self.max_rounds = 100

    def get_auction_state(self):
        return f"Current price: ${self.current_price}"

    def run(self):
        round_count = 0
        while round_count < self.max_rounds:
            auctioneer_action = self.auctioneer.announce_price(self.current_price)
            self.log_action(self.auctioneer, auctioneer_action)

            active_bidders = 0
            for buyer in self.buyers:
                buyer_action = buyer.act(self.get_auction_state())
                self.log_action(buyer, buyer_action)
                if self.process_buyer_action(buyer, buyer_action):
                    active_bidders += 1
            
            if active_bidders == 0:
                break
            elif active_bidders == 1:
                seller_action = self.seller.act(self.get_auction_state())
                self.log_action(self.seller, seller_action)
                self.process_seller_action(seller_action)
                self.close_logger()
                return self.end_auction()
            
            self.current_price += self.increment
            round_count += 1

        self.close_logger()
        return self.end_auction()

    def process_buyer_action(self, buyer, action):
        if action.lower() == "bid":
            if self.current_price <= buyer.budget:
                buyer.last_bid = self.current_price
                return True
            else:
                return False
        return False

    def process_seller_action(self, action):
        self.winner = max(self.buyers, key=lambda b: b.last_bid if hasattr(b, 'last_bid') else 0)
        self.final_price = self.current_price
        return True
