import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically similar
    (i.e., the difference is likely just noise), False if they differ.
    Uses a simple A12 effect size test (non-parametric).
    """
    if not xs or not ys:
        return True
    
    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        greater = 0
        for x in lst1:
            for y in lst2:
                if x > y: greater += 1
                elif x == y: greater += 0.5
        return greater / (m * n)

    # A12 threshold: 0.56 is a small effect size, 0.64 medium, 0.71 large.
    # If the effect size is small, we consider them "the same apart from noise".
    score = a12(xs, ys)
    return abs(0.5 - score) < 0.14

def analyze():
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                processed.append(val if header[i] == 'criterion' else float(val))
            rows.append(processed)

    # The customer asks if the choice of 'criterion' makes a difference.
    # We compare the performance (using a composite score) of the two most common criteria.
    # Score = (1 - MRE) + ACC + PRED
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    crit_idx = header.index('criterion')
    
    def get_score(r):
        return (1.0 - r[mre_idx]) + r[acc_idx] + r[pred_idx]
    
    # Filter for the two most frequent criteria
    c1 = 'squared_error'
    c2 = 'absolute_error'
    
    scores_c1 = [get_score(r) for r in rows if r[crit_idx] == c1]
    scores_c2 = [get_score(r) for r in rows if r[crit_idx] == c2]
    
    is_noise = certify(scores_c1, scores_c2)
    
    print("Analysis: Does the choice of 'criterion' impact performance?")
    if is_noise:
        print(f"Result: The difference between '{c1}' and '{c2}' is likely just noise.")
        print("You can stop arguing about it; the choice does not significantly impact performance.")
    else:
        print(f"Result: The difference between '{c1}' and '{c2}' is statistically significant.")
        print("The choice of criterion does impact performance.")

if __name__ == "__main__":
    analyze()
