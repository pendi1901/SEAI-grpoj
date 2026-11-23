import csv
import math
import step01

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically similar
    (i.e., the difference is likely noise), False if they differ significantly.
    Uses a simple A12 effect size check (non-parametric).
    """
    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        if m == 0 or n == 0: return 0.5
        greater = 0
        for x in lst1:
            for y in lst2:
                if x > y: greater += 1
                elif x == y: greater += 0.5
        return greater / (m * n)

    # If A12 is close to 0.5, they are similar. 
    # Threshold 0.56 is a common small effect size.
    val = a12(xs, ys)
    return 0.44 <= val <= 0.56

def get_data():
    filename = "pom3a.n1000.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(x) for x in row] for row in reader]
    return header, rows

if __name__ == "__main__":
    header, rows = get_data()
    
    # Identify Team Size index and Cost- index
    team_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    # Split into small (bottom 50%) and big (top 50%) teams
    # Using median split on Team Size
    team_sizes = [r[team_idx] for r in rows]
    median_team = sum(team_sizes) / len(team_sizes)
    
    small_teams = [r[cost_idx] for r in rows if r[team_idx] <= median_team]
    big_teams = [r[cost_idx] for r in rows if r[team_idx] > median_team]
    
    is_noise = certify(small_teams, big_teams)
    
    print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
    if is_noise:
        print("Answer: The difference is statistically insignificant; it was likely luck.")
    else:
        avg_small = sum(small_teams) / len(small_teams)
        avg_big = sum(big_teams) / len(big_teams)
        print(f"Answer: The difference is real. Small teams average {avg_small:.4f} vs big teams {avg_big:.4f}.")
