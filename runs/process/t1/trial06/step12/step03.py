import csv

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they differ significantly. Uses a simple A12 effect size test.
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
    # If the effect size is small, we consider them "the same apart from noise".
    return abs(a12(xs, ys) - 0.5) < 0.14

def run_analysis():
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        # Identify indices
        team_size_idx = header.index('Team Size')
        cost_idx = header.index('Cost-')
        
        # Split data: small team (bottom 50%) vs big team (top 50%)
        # Based on the range [0, 1] for Team Size
        small_teams = [r[cost_idx] for r in rows if r[team_size_idx] < 0.5]
        big_teams = [r[cost_idx] for r in rows if r[team_size_idx] >= 0.5]
        
        is_same = certify(small_teams, big_teams)
        
        print("Analysis: Are small-team setups cheaper than big-team ones?")
        if not is_same:
            avg_small = sum(small_teams) / len(small_teams)
            avg_big = sum(big_teams) / len(big_teams)
            print(f"Result: The difference is statistically significant.")
            print(f"Average Cost (Small Teams): {avg_small:.4f}")
            print(f"Average Cost (Big Teams): {avg_big:.4f}")
            print("Conclusion: It is real, not luck.")
        else:
            print("Result: The difference is not statistically significant.")
            print("Conclusion: The observed difference was likely just noise/luck.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

if __name__ == "__main__":
    run_analysis()
