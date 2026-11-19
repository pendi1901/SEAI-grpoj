import csv
from step01 import remember

def get_score(header, row):
    """Calculates the penalty score for a row."""
    goals = [(i, name.endswith('-')) for i, name in enumerate(header) 
             if name.endswith('-') or name.endswith('+')]
    total = 0
    for col_idx, is_min in goals:
        val = float(row[col_idx])
        total += val if is_min else (1.0 - val)
    return total

def justify(header, rows, row):
    """
    Estimates the goal values for the input row using the average of the 
    top 5% of training rows, then calculates the percentile rank.
    """
    # 1. Estimate goal values
    best_indices = remember(header, rows)
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    estimated_row = list(row)
    for g_idx in goal_indices:
        avg_val = sum(rows[i][g_idx] for i in best_indices) / len(best_indices)
        estimated_row[g_idx] = avg_val
    
    # 2. Calculate percentile rank
    target_score = get_score(header, estimated_row)
    better_count = 0
    for r in rows:
        if get_score(header, r) > target_score:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This setup is better than {p:.1%} of all known configurations based on its projected performance metrics."
    
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Use the first row as a test case, masking its goals
        test_row = list(rows[0])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        print(f"Justification: {reason}")
        print(f"Rank: {p:.4f}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
