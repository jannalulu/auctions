import numpy as np

def bid_function(t):
    return 0.5 * t**2

def simulate_all_pay_auction(num_simulations, num_bidders=2):
    total_revenue = 0

    for _ in range(num_simulations):
        # Generate random types for each bidder
        types = np.random.uniform(0, 1, num_bidders)
        
        # Calculate bids for each bidder
        bids = bid_function(types)
        
        # Sum all bids to get the revenue for this auction
        revenue = np.sum(bids)
        
        total_revenue += revenue

    # Calculate average revenue
    expected_revenue = total_revenue / num_simulations
    return expected_revenue

# Run simulation
num_simulations = 1000000
result = simulate_all_pay_auction(num_simulations)

print(f"Simulated expected revenue: {result:.6f}")
print(f"Theoretical expected revenue: {1/3:.6f}")