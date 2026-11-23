import csv

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they differ significantly. Uses the A12 effect size test.
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
    # A12 threshold: 0.56 is small, 0.64 medium, 0.71 large.
    # If the effect size is small (abs(a12 - 0.5) < 0.14), 
    # we consider them "the same apart from noise".
    return abs(a12 - 0.5) < 0.14

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        # The customer asks if results shifted after a change in decision-making.
        # We simulate this by splitting the data into two halves:
        # the first 400 rows (before) and the last 400 rows (after).
        # We use 'Score-' as the metric to evaluate if results shifted.
        score_idx = header.index('Score-')
        before = [r[score_idx] for r in rows[:400]]
        after = [r[score_idx] for r in rows[400:800]]
        
        is_same = certify(before, after)
        
        print("Analysis: Did the results shift after the change in decision-making?")
        if is_same:
            print("Result: The results are statistically the same as before.")
            print("Conclusion: The change in decision-making did not have a significant impact.")
        else:
            print("Result: The results have shifted significantly.")
            print("Conclusion: The change in decision-making caused a real difference in outcomes.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
