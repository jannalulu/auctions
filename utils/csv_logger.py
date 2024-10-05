import csv
from datetime import datetime
import os
import io

class CSVLogger:
    def __init__(self, filename):
        self.filename = filename
        
        # See if file exists
        self.file_exists = os.path.isfile(self.filename)

        # Open file
        self.file = open(self.filename, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        
        # If no file, write a new CSV with the following rows
        if not self.file_exists:
            self.writer.writerow(['Timestamp', 'Agent', 'Action', 'Current Price'])

    # Log actions of buyers and sellers
    def log_action(self, agent, action, current_price):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Catch all encoding errors
        action_encoded = action.encode('utf-8', errors='ignore').decode('utf-8')
        self.writer.writerow([timestamp, agent, action_encoded, current_price])

    # Close file at the end
    def close(self):
        self.file.close()