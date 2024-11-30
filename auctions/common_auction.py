from .base_auction import BaseAuction

class CommonAuction(BaseAuction):
    def __init__(self, item, starting_price, buyers, auctioneer, increment, logger_filename):
        super().__init__(item, starting_price, buyers, auctioneer, logger_filename)
        self.increment = increment
        self.max_rounds = 100
        self.bids = {buyer: 0 for buyer in buyers}  # Track bids for all buyers

    def run(self):
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
            
            if active_bidders == 0:
                break
            elif active_bidders == 1:
                # Determine winner and collect payments
                self.determine_winner_and_payments()
                self.close_logger()
                return self.end_auction()
            
            self.current_price += self.increment
            round_count += 1

        # If we get here, auction ended without a winner
        self.determine_winner_and_payments()
        self.close_logger()
        return self.end_auction()

    def determine_winner_and_payments(self):
        if any(self.bids.values()):
            self.winner = max(self.bids.items(), key=lambda x: x[1])[0]
            self.final_price = self.bids[self.winner]
            
            # Log payments from all bidders who placed bids
            for buyer, bid_amount in self.bids.items():
                if bid_amount > 0:
                    self.log_action(self.auctioneer, f"{buyer.name} pays ${bid_amount}")

    def process_buyer_action(self, buyer, action):
        if action.lower() == "bid":
            if self.current_price <= buyer.budget:
                self.bids[buyer] = self.current_price
                return True
        return False

    def process_seller_action(self, action):
        return True

    def get_auction_state(self):
        return f"Current price: ${self.current_price}"
