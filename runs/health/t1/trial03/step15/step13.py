import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (noise), False if they differ significantly.
    Uses a non-parametric A12 effect size test.
    """
    if not xs or not ys:
        return True
    
    def count_greater(list1, list2):
        count = 0
        for x in list1:
            for y in list2:
                if x > y:
                    count += 1
                elif x == y:
                    count += 0.5
        return count

    n, m = len(xs), len(ys)
    a12 = count_greater(xs, ys) / (n * m)
    
    # A12 threshold: 0.56 is small, 0.64 is medium, 0.71 is large.
    # If A12 is close to 0.5, they are likely the same (noise).
    # We use 0.14 as the threshold for "significant" difference.
    return abs(a12 - 0.5) < 0.14

def analyze_criterion(header, rows):
    """
    Compares the performance (aggregate score) of different 'criterion' settings.
    """
    crit_idx = header.index('criterion')
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    # Normalize goals to create a single performance score
    def get_score(row):
        s = 0
        for i in goal_indices:
            col = header[i]
            vals = [r[i] for r in rows]
            mn, mx = min(vals), max(vals)
            norm = (row[i] - mn) / (mx - mn) if mx > mn else 0
            s += (1 - norm) if col.endswith('-') else norm
        return s

    # Group scores by criterion
    groups = {}
    for row in rows:
        c = row[crit_idx]
        if c not in groups: groups[c] = []
        groups[c].append(get_score(row))
    
    # Compare the two most common criteria (e.g., squared_error vs absolute_error)
    keys = list(groups.keys())
    if len(keys) < 2:
        return True, "Not enough variety in criteria to compare."
    
    is_noise = certify(groups[keys[0]], groups[keys[1]])
    return is_noise, f"Comparison between {keys[0]} and {keys[1]}"

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)
            
    is_noise, details = analyze_criterion(header, rows)
    
    print(f"Analysis: {details}")
    if is_noise:
        print("Conclusion: The choice of criterion makes no real difference; it is just noise.")
    else:
        print("Conclusion: The choice of criterion makes a statistically significant difference.")
