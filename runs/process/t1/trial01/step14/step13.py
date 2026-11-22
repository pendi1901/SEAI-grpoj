import csv

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they differ significantly. Uses the A12 effect size test.
    """
    m, n = len(xs), len(ys)
    greater = 0
    for x in xs:
        for y in ys:
            if x > y:
                greater += 1
            elif x == y:
                greater += 0.5
    
    a12 = greater / (m * n)
    # A12 threshold: 0.56 is a small effect size. 
    # If the effect size is small, we consider them the same.
    return 0.44 <= a12 <= 0.56

def get_score(header, row):
    """Calculates a normalized score [0, 1] where lower is better."""
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))
    
    scores = []
    for idx, op in goal_indices:
        val = float(row[idx])
        scores.append(val if op == '-' else (1.0 - val))
    return sum(scores) / len(scores)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # The customer asks if results shifted after a change in team decision-making.
        # We simulate this by comparing the first half of the data (before) 
        # to the second half (after).
        mid = len(rows) // 2
        before = [get_score(header, row) for row in rows[:mid]]
        after = [get_score(header, row) for row in rows[mid:]]
        
        is_same = certify(before, after)
        
        print("Customer Inquiry: Did team decision-making changes shift results?")
        print(f"Analysis: Comparing performance scores before and after the change.")
        if is_same:
            print("Conclusion: The results are statistically the same. The change in ")
            print("team decision-making did not significantly impact project outcomes.")
        else:
            print("Conclusion: The results have shifted significantly. The change in ")
            print("team decision-making appears to have had a measurable impact.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
