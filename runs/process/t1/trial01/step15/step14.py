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

def flow(header, row, seen):
    """
    Warns the customer when a new row is significantly worse than the 
    historical average performance.
    """
    if not seen:
        return False
    
    # Calculate the average performance of all seen rows
    scores = [get_score(header, r) for r in seen]
    avg_score = sum(scores) / len(scores)
    
    # Calculate standard deviation of seen scores
    variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
    std_dev = variance ** 0.5
    
    # If the new row's score is more than 1 standard deviation worse 
    # than the average, we flag it as "going bad".
    current_score = get_score(header, row)
    
    # Return True if the performance is degrading (score is higher than average + threshold)
    return current_score > (avg_score + std_dev)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        seen = []
        warnings = 0
        for row in rows:
            if flow(header, row, seen):
                warnings += 1
            seen.append(row)
            
        print("Customer Inquiry: Monitoring Project Performance")
        print(f"Analysis: Processed {len(rows)} weekly reports.")
        print(f"Warning: {warnings} reports indicated a significant decline in performance.")
        print("Strategy: Flagged any report where the performance score exceeded")
        print("the historical average by more than one standard deviation.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
