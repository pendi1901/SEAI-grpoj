import ezr
import step01

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    """
    # Using the statistical tests provided in ezr.stats
    # same() checks cliffs, ks, and cohen's d.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load data
    file_path = "pom3a.train.csv"
    rows_iter = ezr.csv(file_path)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # Find index for 'Team Size' and 'Cost-'
    team_idx = header.index("Team Size")
    cost_idx = header.index("Cost-")
    
    # Define small vs big teams (split by median team size)
    team_sizes = [r[team_idx] for r in all_rows]
    median_team = sorted(team_sizes)[len(team_sizes) // 2]
    
    small_team_costs = [r[cost_idx] for r in all_rows if r[team_idx] <= median_team]
    big_team_costs = [r[cost_idx] for r in all_rows if r[team_idx] > median_team]
    
    # Perform certification
    is_same = certify(small_team_costs, big_team_costs)
    
    print(f"Analysis of {len(all_rows)} records:")
    print(f"Small teams (<= {median_team}): {len(small_team_costs)} records")
    print(f"Big teams (> {median_team}): {len(big_team_costs)} records")
    
    if is_same:
        print("Result: The difference in costs is statistically insignificant (likely luck).")
    else:
        print("Result: The difference in costs is statistically significant (it is real).")
    
    exit(0)
