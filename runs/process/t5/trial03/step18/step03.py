import ezr
import random

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they are significantly different.
    Uses the same logic as ezr.same (cliffs and ks tests).
    """
    return ezr.same(xs, ys)

def analyze():
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Find indices
    team_size_idx = header.index("Team Size")
    cost_idx = header.index("Cost-")
    
    # Split data into small-team and big-team groups
    # Median split on Team Size
    team_sizes = [r[team_size_idx] for r in rows]
    median_size = sorted(team_sizes)[len(team_sizes) // 2]
    
    small_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] <= median_size]
    big_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] > median_size]
    
    # Perform certification
    is_same = certify(small_team_costs, big_team_costs)
    
    print("Analysis: Comparing 'Cost-' for small vs big teams.")
    print(f"Small team count: {len(small_team_costs)}, Big team count: {len(big_team_costs)}")
    print(f"Mean Cost (Small): {sum(small_team_costs)/len(small_team_costs):.4f}")
    print(f"Mean Cost (Big):   {sum(big_team_costs)/len(big_team_costs):.4f}")
    
    if is_same:
        print("Result: The difference is statistically insignificant. It was likely luck.")
    else:
        print("Result: The difference is statistically significant. The observation is real.")

if __name__ == "__main__":
    analyze()
