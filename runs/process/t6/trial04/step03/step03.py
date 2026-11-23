import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    # ezr.same uses cliffs and ks tests to check if distributions differ.
    return ezr.same(xs, ys)

def get_team_data(header, rows):
    """
    Splits the data into 'small' and 'big' teams based on the median Team Size.
    Returns the Cost- values for each group.
    """
    team_idx = header.index("Team Size")
    cost_idx = header.index("Cost-")
    
    team_sizes = [r[team_idx] for r in rows]
    median = sorted(team_sizes)[len(team_sizes) // 2]
    
    small_costs = [r[cost_idx] for r in rows if r[team_idx] <= median]
    big_costs = [r[cost_idx] for r in rows if r[team_idx] > median]
    
    return small_costs, big_costs

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    small, big = get_team_data(header, rows)
    
    is_same = certify(small, big)
    
    print("Analysis: Are small-team setups cheaper than big-team ones?")
    print("-" * 60)
    print(f"Small team average cost: {sum(small)/len(small):.4f}")
    print(f"Big team average cost:   {sum(big)/len(big):.4f}")
    print("-" * 60)
    
    if is_same:
        print("Result: The difference is statistically insignificant (likely luck).")
    else:
        print("Result: The difference is statistically significant (it is real).")
