import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    # Use ezr's statistical tests: same() checks cliffs and ks
    # We use the default effect size (eps=0) to check for difference.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Identify column indices
    # 'Team Size' is at index 8, 'Cost-' is at index 9
    team_size_idx = 8
    cost_idx = 9
    
    # Define small vs big teams based on the median team size
    team_sizes = [r[team_size_idx] for r in rows]
    median_size = sorted(team_sizes)[len(team_sizes) // 2]
    
    small_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] <= median_size]
    big_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] > median_size]
    
    # Perform certification
    is_same = certify(small_team_costs, big_team_costs)
    
    print(f"Analysis of Cost- vs Team Size:")
    print(f"Small team count: {len(small_team_costs)}, Big team count: {len(big_team_costs)}")
    print(f"Small team avg cost: {sum(small_team_costs)/len(small_team_costs):.4f}")
    print(f"Big team avg cost: {sum(big_team_costs)/len(big_team_costs):.4f}")
    
    if is_same:
        print("Result: The difference is statistically insignificant (it was likely luck).")
    else:
        print("Result: The difference is statistically significant (it is real).")
        
    exit(0)
