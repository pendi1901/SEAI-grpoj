import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (same apart from noise), False otherwise.
    """
    return ezr.same(xs, ys)

def analyze():
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Find index for 'Team Size' and 'Cost-'
    team_idx = header.index("Team Size")
    cost_idx = header.index("Cost-")
    
    # Split into small team (<= 0.5) and big team (> 0.5)
    # Based on the normalized range [0, 1]
    small_teams = [r[cost_idx] for r in rows if r[team_idx] <= 0.5]
    big_teams = [r[cost_idx] for r in rows if r[team_idx] > 0.5]
    
    # Check if they are statistically different
    is_same = certify(small_teams, big_teams)
    
    print("Analysis: Are small-team setups cheaper than big-team ones?")
    if not is_same:
        print("Result: The difference is statistically significant (not just luck).")
    else:
        print("Result: The difference is not statistically significant (likely just noise).")
    
    print(f"Small team avg cost: {sum(small_teams)/len(small_teams):.3f}")
    print(f"Big team avg cost:   {sum(big_teams)/len(big_teams):.3f}")

if __name__ == "__main__":
    analyze()
    exit(0)
