import csv

def justify(header, rows, row):
    """
    Returns (p, reason) where p is the fraction of rows that 'row' is better than,
    and reason explains why 'row' is not as good as the best known configuration.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]

    def get_score(r):
        score = 0.0
        for i in goal_indices:
            val = r[i]
            # Normalize: '-' minimized, '+' maximized
            if header[i].endswith('-'):
                score += val
            else:
                score += (1.0 - val)
        return score

    # 1. Estimate the goals for the provided 'row' using 1-nearest neighbor
    best_dist = float('inf')
    best_match = None
    for train_row in rows:
        dist = sum((row[i] - train_row[i])**2 for i in input_indices)
        if dist < best_dist:
            best_dist = dist
            best_match = train_row
    
    # Create a copy of the row with estimated goals
    estimated_row = list(row)
    for i in goal_indices:
        estimated_row[i] = best_match[i]
    
    # 2. Calculate percentile rank
    my_score = get_score(estimated_row)
    better_count = sum(1 for r in rows if get_score(r) < my_score)
    p = better_count / len(rows)
    
    # 3. Find the best row in the dataset to compare against
    best_overall = min(rows, key=get_score)
    best_score = get_score(best_overall)
    
    # 4. Construct the reason
    # Identify which goal is the biggest contributor to the score difference
    diffs = []
    for i in goal_indices:
        diff = abs(estimated_row[i] - best_overall[i])
        diffs.append((diff, header[i]))
    diffs.sort(key=lambda x: x[0], reverse=True)
    
    reason = (f"Your setup is better than {p:.4f} of configurations, but it is "
              f"outperformed by the best setup primarily due to differences in {diffs[0][1]}.")
    
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Simulate a user providing a row (e.g., the 50th row) and asking about it
        sample_row = list(rows[50])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        
        print("Customer Inquiry: Why is this setup not the best?")
        print("-" * 60)
        print(f"Performance Rank: {p:.4f}")
        print(f"Explanation: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
