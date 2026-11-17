import ezr
import random

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    # Using the same logic as ezr.same, which checks for 
    # statistical significance using Cliff's Delta and KS test.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    # Identify column indices
    # Team Size is at index 8, Cost- is at index 9
    team_size_idx = 8
    cost_idx = 9
    
    # Calculate the median team size to split into "small" and "big"
    team_sizes = [r[team_size_idx] for r in rows]
    median_team = sorted(team_sizes)[len(team_sizes) // 2]
    
    small_team_costs = []
    big_team_costs = []
    
    for row in rows:
        if row[team_size_idx] <= median_team:
            small_team_costs.append(row[cost_idx])
        else:
            big_team_costs.append(row[cost_idx])
            
    # Perform certification
    is_same = certify(small_team_costs, big_team_costs)
    
    print("Analysis: Are small-team setups cheaper than big-team ones?")
    print(f"Small team median cost: {sorted(small_team_costs)[len(small_team_costs)//2]:.4f}")
    print(f"Big team median cost:   {sorted(big_team_costs)[len(big_team_costs)//2]:.4f}")
    
    if is_same:
        print("Result: The difference is statistically insignificant (it was likely luck).")
    else:
        print("Result: The difference is statistically significant (it is real).")
        
    exit(0)
