import ezr
import random

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    """
    # Use ezr's same function which combines cliffs, ks, and cohen tests.
    # We use the default effect size (0.35 for cohen, 0.197 for cliffs).
    return ezr.same(xs, ys, eps=0.35)

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Find indices for 'Team Size' and 'Cost-'
    # 'Team Size' is index 8, 'Cost-' is index 9
    team_idx = header.index("Team Size")
    cost_idx = header.index("Cost-")
    
    # Define "small" as below median, "big" as above median
    team_sizes = [r[team_idx] for r in rows]
    median_team = sorted(team_sizes)[len(team_sizes) // 2]
    
    small_team_costs = [r[cost_idx] for r in rows if r[team_idx] <= median_team]
    big_team_costs = [r[cost_idx] for r in rows if r[team_idx] > median_team]
    
    # Perform certification
    is_same = certify(small_team_costs, big_team_costs)
    
    print("Certification: Are small-team costs different from big-team costs?")
    print("-" * 60)
    print(f"Small team count: {len(small_team_costs)}, Avg Cost: {sum(small_team_costs)/len(small_team_costs):.4f}")
    print(f"Big team count:   {len(big_team_costs)}, Avg Cost: {sum(big_team_costs)/len(big_team_costs):.4f}")
    print("-" * 60)
    
    if is_same:
        print("Result: The difference is statistically insignificant (it was likely luck).")
    else:
        print("Result: The difference is statistically significant (it is real).")
        
    exit(0)
