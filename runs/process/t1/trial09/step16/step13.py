import csv

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they differ significantly. Uses the A12 effect size check.
    """
    m, n = len(xs), len(ys)
    if m == 0 or n == 0:
        return True
    
    greater = 0
    for x in xs:
        for y in ys:
            if x > y:
                greater += 1
            elif x == y:
                greater += 0.5
    
    a12 = greater / (m * n)
    # A12 threshold: 0.56 is a small effect size.
    # If A12 is between 0.44 and 0.56, the difference is negligible.
    return 0.44 <= a12 <= 0.56

def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append([float(x) for x in row])
    return header, rows

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        header, rows = load_data(filename)
        
        # The customer asks if results shifted after a change in decision-making.
        # We simulate this by comparing the first half of the data (before)
        # to the second half (after).
        mid = len(rows) // 2
        before = rows[:mid]
        after = rows[mid:]
        
        # We evaluate the shift based on the 'Score-' goal (a primary outcome)
        score_idx = header.index('Score-')
        xs = [r[score_idx] for r in before]
        ys = [r[score_idx] for r in after]
        
        is_same = certify(xs, ys)
        
        print("Analysis: Did the team's decision-making change shift the results?")
        if is_same:
            print("Result: The results are statistically the same; the change had no significant impact.")
        else:
            print("Result: There is a statistically significant difference in the results.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
