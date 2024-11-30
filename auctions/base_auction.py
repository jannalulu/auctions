from abc import ABC, abstractmethod
from utils.csv_logger import CSVLogger

class BaseAuction(ABC):
    def __init__(self, item, starting_price, buyers, auctioneer, logger_filename):
        self.item = item
        self.current_price = starting_price
        self.buyers = buyers
        self.auctioneer = auctioneer
        self.logger = CSVLogger(logger_filename)
        self.winner = None
        self.final_price = None

    @abstractmethod
    def run(self):
        pass

    def log_action(self, agent, action):
        self.logger.log_action(agent.name, action, self.current_price)
        agent.add_to_history(f"Price ${self.current_price}: {action}")
        print(f"{agent.name}: {action} (Current price: ${self.current_price})")

    def close_logger(self):
        self.logger.close()

    def get_auction_state(self):
        return f"Current price: ${self.current_price}"

    @abstractmethod
    def process_buyer_action(self, buyer, action):
        pass

    @abstractmethod
    def process_seller_action(self, action):
        pass

    def end_auction(self):
        if self.winner:
            return {
                "winner": self.winner.name,
                "final_price": self.final_price
            }
        else:
            return {
                "winner": None,
                "final_price": None,
                "result": "No sale"
            }