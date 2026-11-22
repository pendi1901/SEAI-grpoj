import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (same apart from noise), False otherwise.
    Uses the Vargha-Delaney A12 effect size check.
    """
    if not xs or not ys:
        return True
    
    n_x, n_y = len(xs), len(ys)
    greater = 0
    equal = 0
    for x in xs:
        for y in ys:
            if x > y:
                greater += 1
            elif x == y:
                equal += 1
                
    a12 = (greater + 0.5 * equal) / (n_x * n_y)
    
    # A12 threshold: 0.56 is a small effect size.
    # If A12 is between 0.44 and 0.56, they are effectively the same.
    return 0.44 <= a12 <= 0.56

def analyze_rules(header, rows):
    """
    Compares the performance of rows using different 'criterion' settings.
    We focus on the primary goal MRE- (minimize).
    """
    idx_crit = header.index('criterion')
    idx_mre = header.index('MRE-')
    
    # Get unique criteria
    criteria = list(set(r[idx_crit] for r in rows))
    
    # Group MRE values by criterion
    groups = {c: [] for c in criteria}
    for r in rows:
        groups[r[idx_crit]].append(r[idx_mre])
        
    # Compare each pair of criteria
    results = {}
    for i in range(len(criteria)):
        for j in range(i + 1, len(criteria)):
            c1, c2 = criteria[i], criteria[j]
            is_same = certify(groups[c1], groups[c2])
            results[(c1, c2)] = is_same
            
    return results

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] == 'criterion':
                        processed.append(val)
                    else:
                        processed.append(float(val))
                rows.append(processed)
        
        comparisons = analyze_rules(header, rows)
        
        print("Analysis: Does the choice of 'criterion' make a difference?")
        all_same = True
        for (c1, c2), is_same in comparisons.items():
            if not is_same:
                all_same = False
                print(f"Significant difference found between {c1} and {c2}.")
        
        if all_same:
            print("Conclusion: The choice of criterion does not make a real difference. You can stop arguing about it.")
        else:
            print("Conclusion: There are statistically significant differences between some criteria.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
