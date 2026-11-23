import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (the same apart from noise), False otherwise.
    Uses the A12 effect size test (Vargha-Delaney).
    """
    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        if m == 0 or n == 0: return 0.5
        
        # Count how many times items in lst1 are greater than items in lst2
        greater = 0
        for x in lst1:
            for y in lst2:
                if x > y: greater += 1
                elif x == y: greater += 0.5
        
        return greater / (m * n)

    # A12 threshold: 0.56 is a small effect size, 0.64 medium, 0.71 large.
    # If A12 is close to 0.5, they are effectively the same.
    score = a12(xs, ys)
    return 0.44 <= score <= 0.56

def run_analysis():
    filename = "pom3a.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])

    # Identify indices
    team_size_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')

    # Split into small-team (below median) and big-team (above median)
    team_sizes = [r[team_size_idx] for r in rows]
    median_size = sum(team_sizes) / len(team_sizes)
    
    small_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] < median_size]
    big_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] >= median_size]

    is_same = certify(small_team_costs, big_team_costs)

    print("Analysis: Comparing costs of small-team vs big-team setups.")
    if is_same:
        print("Result: The difference in costs is statistically insignificant.")
        print("Conclusion: The observation was likely due to luck, not a real trend.")
    else:
        print("Result: There is a statistically significant difference in costs.")
        print("Conclusion: Small-team setups are genuinely different in cost performance.")

if __name__ == "__main__":
    try:
        run_analysis()
    except FileNotFoundError:
        print("Error: pom3a.n1000.train.csv not found.")
        exit(1)
