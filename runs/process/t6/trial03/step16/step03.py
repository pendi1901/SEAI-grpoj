import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable,
    False if they differ significantly.
    """
    return ezr.same(xs, ys)

def analyze():
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Find index for 'Team Size' (input) and 'Cost-' (goal)
    team_idx = header.index("Team Size")
    cost_idx = header.index("Cost-")
    
    # Split into small team (<= 0.5) and big team (> 0.5)
    # Based on the normalized range [0, 1]
    small_teams = [r[cost_idx] for r in rows if r[team_idx] <= 0.5]
    big_teams = [r[cost_idx] for r in rows if r[team_idx] > 0.5]
    
    # Check if they are the same
    is_same = certify(small_teams, big_teams)
    
    print("Analysis: Are small-team setups cheaper than big-team ones?")
    print(f"Small team cost mean: {sum(small_teams)/len(small_teams):.4f}")
    print(f"Big team cost mean:   {sum(big_teams)/len(big_teams):.4f}")
    
    if is_same:
        print("Result: The difference is statistically insignificant (it was likely luck).")
    else:
        print("Result: The difference is statistically significant (it is real).")

if __name__ == "__main__":
    analyze()
