import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (same apart from noise), False if they differ.
    """
    # Use the stats functions from ezr to check if the distributions are the same.
    # same() checks cliffs delta and KS test, and optionally Cohen's d.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify index for 'Team Size' (input) and 'Cost-' (goal)
    # header = ['Culture', 'Criticality', 'Criticality Modifier', 'Initial Known', 
    #           'Inter-Dependency', 'Dynamism', 'Size', 'Plan', 'Team Size', 
    #           'Cost-', 'Score-', 'Idle-']
    team_size_idx = 8
    cost_idx = 9
    
    # Split into small-team and big-team based on median Team Size
    team_sizes = [r[team_size_idx] for r in rows]
    median_team = sum(team_sizes) / len(team_sizes)
    
    small_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] < median_team]
    big_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] >= median_team]
    
    # Certify if the difference is real
    is_same = certify(small_team_costs, big_team_costs)
    
    print("Analysis: Are small-team setups cheaper than big-team ones?")
    if not is_same:
        print("Result: The difference is statistically significant (not just luck).")
    else:
        print("Result: The difference is not statistically significant (likely luck).")
    
    print(f"Small team avg cost: {sum(small_team_costs)/len(small_team_costs):.4f}")
    print(f"Big team avg cost:   {sum(big_team_costs)/len(big_team_costs):.4f}")
