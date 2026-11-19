import csv

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

def justify(header, rows, row):
    """
    Estimates the performance of 'row' by finding its nearest neighbor in 'rows',
    then calculates what fraction of 'rows' are worse than this estimate.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith(('-', '+')))]
    
    # Estimate the missing goals using 1-Nearest Neighbor
    best_dist = float('inf')
    best_row = None
    for r in rows:
        dist = sum((float(row[i]) - float(r[i]))**2 for i in input_indices)
        if dist < best_dist:
            best_dist = dist
            best_row = r
            
    estimated_score = get_score(header, best_row)
    
    # Calculate how many rows are worse (have a higher score) than our estimate
    all_scores = [get_score(header, r) for r in rows]
    worse_count = sum(1 for s in all_scores if s > estimated_score)
    p = worse_count / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all possible configurations based on its similarity to known high-performing data."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        # Pick a sample row and mask its goals
        sample_row = list(rows[0])
        for i, name in enumerate(header):
            if name.endswith(('-', '+')):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        print(f"Justification Analysis:")
        print(f"Rank: {p:.4f}")
        print(f"Reason: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
