import ezr
import random

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    """
    return ezr.same(sorted(xs), sorted(ys), eps=0.35)

def analyze():
    # Load data
    data = list(ezr.csv("pom3a.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Identify indices
    team_size_idx = header.index("Team Size")
    cost_idx = header.index("Cost-")
    
    # Split into small vs big teams (median split)
    team_sizes = [r[team_size_idx] for r in rows]
    median_size = sorted(team_sizes)[len(team_sizes) // 2]
    
    small_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] <= median_size]
    big_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] > median_size]
    
    # Certify difference
    is_same = certify(small_team_costs, big_team_costs)
    
    print("Analysis of Team Size vs Cost:")
    print(f"Small team count: {len(small_team_costs)}, Big team count: {len(big_team_costs)}")
    print(f"Small team avg cost: {sum(small_team_costs)/len(small_team_costs):.4f}")
    print(f"Big team avg cost: {sum(big_team_costs)/len(big_team_costs):.4f}")
    
    if is_same:
        print("Conclusion: The difference in costs is statistically insignificant (likely luck).")
    else:
        print("Conclusion: There is a statistically significant difference in costs.")

if __name__ == "__main__":
    analyze()
    exit(0)
