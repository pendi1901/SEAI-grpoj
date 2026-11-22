import csv

def justify(header, rows, row):
    """
    Estimates the performance of a row and returns its percentile rank
    against the training data, along with a justification.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def get_score(r):
        # Calculate a normalized score: lower is better.
        # For '-', we want low values. For '+', we want high values (1-val).
        total = 0.0
        for idx, op in goal_indices:
            val = float(r[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # Estimate missing goals using 1-Nearest Neighbor
    best_dist = float('inf')
    best_row = None
    for train_row in rows:
        dist = sum((float(row[i]) - float(train_row[i]))**2 for i in input_indices)
        if dist < best_dist:
            best_dist = dist
            best_row = train_row
    
    # Create a copy of the row with estimated goals
    estimated_row = list(row)
    for idx, _ in goal_indices:
        estimated_row[idx] = best_row[idx]
    
    # Compare against all rows
    my_score = get_score(estimated_row)
    better_count = sum(1 for r in rows if get_score(r) < my_score)
    p = better_count / len(rows)
    
    reason = f"This setup is better than {p:.0%} of all known configurations based on its estimated performance metrics."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            # Create a test row by masking goals of the first row
            test_row = list(rows[0])
            for i in range(len(header)):
                if header[i].endswith('-') or header[i].endswith('+'):
                    test_row[i] = "?"
            
            p, reason = justify(header, rows, test_row)
            
            print("Customer Inquiry: How does this setup rank?")
            print(f"Rank: {p:.4f}")
            print(f"Justification: {reason}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
