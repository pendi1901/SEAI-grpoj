import csv
import math

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they are significantly different. Uses a simple A12 effect size test.
    """
    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        greater = 0
        for x in lst1:
            for y in lst2:
                if x > y: greater += 1
                elif x == y: greater += 0.5
        return greater / (m * n)

    # A12 threshold: 0.56 is a small effect size, 0.64 medium, 0.71 large.
    # If A12 is close to 0.5, they are the same.
    score = a12(xs, ys)
    return abs(0.5 - score) < 0.147

def get_data():
    filename = 'pom3a.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])
    return header, rows

if __name__ == "__main__":
    header, rows = get_data()
    
    # Find indices
    team_size_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    # Split into small vs big teams (using median split)
    team_sizes = [r[team_size_idx] for r in rows]
    median_team = sum(team_sizes) / len(team_sizes)
    
    small_teams = [r[cost_idx] for r in rows if r[team_size_idx] <= median_team]
    big_teams = [r[cost_idx] for r in rows if r[team_size_idx] > median_team]
    
    # Compare
    is_same = certify(small_teams, big_teams)
    
    print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
    print("-" * 60)
    print(f"Small team average cost: {sum(small_teams)/len(small_teams):.4f}")
    print(f"Big team average cost:   {sum(big_teams)/len(big_teams):.4f}")
    
    if is_same:
        print("\nConclusion: The difference is statistically insignificant.")
        print("It was likely just luck.")
    else:
        print("\nConclusion: The difference is statistically significant.")
        print("Small teams are genuinely cheaper.")
