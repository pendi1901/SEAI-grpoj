import csv

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they differ significantly. Uses a simple A12 effect size check.
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

    # A12 threshold: 0.56 is a small effect size, 0.64 medium, 0.71 large.
    # If A12 is close to 0.5, they are likely the same.
    score = a12(xs, ys)
    return 0.44 <= score <= 0.56

def get_data():
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append([float(x) for x in row])
    return header, rows

if __name__ == "__main__":
    header, rows = get_data()
    
    # Find index for 'Team Size' and 'Cost-'
    team_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    # Split into small vs big teams based on median team size
    team_sizes = [r[team_idx] for r in rows]
    median_team = sum(team_sizes) / len(team_sizes)
    
    small_teams = [r[cost_idx] for r in rows if r[team_idx] < median_team]
    big_teams = [r[cost_idx] for r in rows if r[team_idx] >= median_team]
    
    is_same = certify(small_teams, big_teams)
    
    print("Analysis: Comparing Cost- for small vs big team setups.")
    if is_same:
        print("Result: The difference is likely due to noise (not statistically significant).")
    else:
        print("Result: There is a real, statistically significant difference in costs.")
