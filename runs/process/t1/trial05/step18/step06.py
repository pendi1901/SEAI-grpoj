import csv

def justify(header, rows, row):
    """
    Estimates the performance of a given row by finding the nearest neighbor
    in the training data, then calculates its percentile rank against all rows.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    def get_score(r):
        total = 0
        for i in goal_indices:
            val = float(r[i])
            if header[i].endswith('-'):
                total += val
            else:
                total += (1.0 - val)
        return total

    # Estimate goals for the input row using 1-nearest neighbor
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            d += (float(r1[i]) - float(r2[i])) ** 2
        return d ** 0.5

    best_dist = float('inf')
    best_row = None
    for r in rows:
        d = dist(row, r)
        if d < best_dist:
            best_dist = d
            best_row = r
            
    # Use the estimated score based on the nearest neighbor's goal values
    estimated_score = get_score(best_row)
    
    # Calculate percentile rank: fraction of rows better than this one
    all_scores = [get_score(r) for r in rows]
    better_count = sum(1 for s in all_scores if s < estimated_score)
    p = better_count / len(rows)
    
    reason = f"This setup is estimated to be better than {int(p * 100)}% of all known configurations based on its similarity to high-performing historical data."
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
        
        # Pick an example row and mask its goals
        test_row = list(rows[0])
        for i in range(len(test_row)):
            if header[i].endswith('-') or header[i].endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        
        print("Customer Inquiry: How does this setup rank?")
        print("-" * 60)
        print(f"Rank: {p:.4f}")
        print(f"Justification: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
