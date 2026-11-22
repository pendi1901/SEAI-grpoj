import csv

def certify(xs, ys):
    """
    Determines if two distributions are statistically similar using a 
    non-parametric approach (Mann-Whitney U test logic).
    Returns True if they are the same apart from noise, False if they differ.
    """
    n1, n2 = len(xs), len(ys)
    if n1 == 0 or n2 == 0:
        return True
    
    # Combine and rank
    combined = sorted([(x, 0) for x in xs] + [(y, 1) for y in ys])
    ranks = {}
    for i, (val, group) in enumerate(combined):
        ranks.setdefault(val, []).append(i + 1)
    
    # Assign average rank for ties
    avg_ranks = {val: sum(r) / len(r) for val, r in ranks.items()}
    
    rank_sum_x = sum(avg_ranks[x] for x in xs)
    
    # U statistic
    u1 = rank_sum_x - (n1 * (n1 + 1)) / 2
    u2 = (n1 * n2) - u1
    u = min(u1, u2)
    
    # Normal approximation for large samples
    mu = (n1 * n2) / 2
    sigma = ((n1 * n2 * (n1 + n2 + 1)) / 12) ** 0.5
    
    if sigma == 0:
        return True
        
    z = abs(u - mu) / sigma
    # Critical value for 95% confidence (z=1.96)
    return z < 1.96

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # The customer asks about the "two built-in rules". 
        # In this dataset, the 'criterion' column has 3 values, but 'absolute_error' 
        # and 'squared_error' are the primary ones used in the provided examples.
        # We compare the ACC+ performance of these two rules.
        crit_idx = header.index('criterion')
        acc_idx = header.index('ACC+')
        
        abs_err = [r[acc_idx] for r in rows if r[crit_idx] == 'absolute_error']
        sq_err = [r[acc_idx] for r in rows if r[crit_idx] == 'squared_error']
        
        is_same = certify(abs_err, sq_err)
        
        print("Analysis: Comparing 'absolute_error' vs 'squared_error' criteria.")
        if is_same:
            print("Result: The difference is statistically insignificant.")
            print("Answer: You can stop arguing; the choice does not make a real difference.")
        else:
            print("Result: There is a statistically significant difference.")
            print("Answer: The choice matters; you should choose the rule that performs better.")
        exit(0)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
