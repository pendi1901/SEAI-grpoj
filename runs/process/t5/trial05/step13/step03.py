import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    # Use the same logic as ezr.same, which checks for statistical significance
    # using Cliff's Delta and the Kolmogorov-Smirnov test.
    return ezr.same(xs, ys)

def get_team_data(header, rows):
    """
    Splits the data into two groups based on 'Team Size'.
    'Team Size' is a numeric column (starts with uppercase).
    We split at the median to compare 'small' vs 'big' teams.
    """
    team_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    # Filter out rows with missing data
    valid_rows = [r for r in rows if r[team_idx] != "?"]
    team_sizes = [r[team_idx] for r in valid_rows]
    median = sorted(team_sizes)[len(team_sizes) // 2]
    
    small_teams = [r[cost_idx] for r in valid_rows if r[team_idx] <= median]
    big_teams = [r[cost_idx] for r in valid_rows if r[team_idx] > median]
    
    return small_teams, big_teams

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    small, big = get_team_data(header, rows)
    
    # Perform the certification
    is_same = certify(small, big)
    
    print(f"Analysis of Cost- for small vs big teams:")
    print(f"Small team count: {len(small)}, Big team count: {len(big)}")
    print(f"Average Cost- (small): {sum(small)/len(small):.4f}")
    print(f"Average Cost- (big):   {sum(big)/len(big):.4f}")
    
    if is_same:
        print("Conclusion: The difference is statistically insignificant (it was likely luck).")
    else:
        print("Conclusion: The difference is statistically significant (it is real).")
