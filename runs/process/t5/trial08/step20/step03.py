import ezr
import random

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    """
    # Use ezr.same which combines cliffs, ks, and cohen tests
    return ezr.same(xs, ys, eps=0.35)

def analyze(header, rows):
    """
    Compare Cost- for small teams (Team Size < 0.5) vs big teams (Team Size >= 0.5).
    """
    # Find column indices
    team_size_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    small_teams = []
    big_teams = []
    
    for row in rows:
        if row[team_size_idx] < 0.5:
            small_teams.append(row[cost_idx])
        else:
            big_teams.append(row[cost_idx])
            
    # Perform statistical test
    is_same = certify(small_teams, big_teams)
    
    return small_teams, big_teams, is_same

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty or missing.")
        exit(1)
        
    small, big, is_same = analyze(header, rows)
    
    avg_small = sum(small) / len(small)
    avg_big = sum(big) / len(big)
    
    print(f"Analysis of Cost- by Team Size:")
    print(f"  Small teams (n={len(small)}): avg cost = {avg_small:.4f}")
    print(f"  Big teams   (n={len(big)}): avg cost = {avg_big:.4f}")
    
    if is_same:
        print("\nConclusion: The difference is statistically insignificant. It was likely luck.")
    else:
        print("\nConclusion: The difference is statistically significant. It is a real effect.")
        
    exit(0)
