import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable,
    False if they differ significantly.
    """
    # ezr.same performs cliffs delta and ks test, 
    # which are robust for comparing two distributions.
    return ezr.same(xs, ys)

def analyze(header, rows):
    """
    Splits data into small-team (Team Size < 0.5) and big-team (Team Size >= 0.5)
    and compares their 'Cost-' values.
    """
    # Team Size is at index 8
    team_size_idx = 8
    cost_idx = 9
    
    small_teams = []
    big_teams = []
    
    for row in rows:
        if row[team_size_idx] == "?":
            continue
        if row[team_size_idx] < 0.5:
            small_teams.append(row[cost_idx])
        else:
            big_teams.append(row[cost_idx])
            
    is_same = certify(small_teams, big_teams)
    
    print(f"Small team cost mean: {sum(small_teams)/len(small_teams):.4f}")
    print(f"Big team cost mean:   {sum(big_teams)/len(big_teams):.4f}")
    
    if is_same:
        print("Result: The difference is likely due to luck (not statistically significant).")
    else:
        print("Result: The difference is statistically significant.")
    
    return is_same

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    try:
        header = next(rows_gen)
        rows = list(rows_gen)
        analyze(header, rows)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    exit(0)
