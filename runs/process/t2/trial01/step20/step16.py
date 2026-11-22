import csv
from step01 import remember
from step06 import get_score

def justify(header, rows, row):
    """
    Explains why a specific setup (row) might not be the best choice by 
    comparing its performance rank against the entire dataset.
    """
    # 1. Estimate goal values for the input row
    # We find the 5 most similar rows to estimate the missing goals
    from step11 import find_similar
    
    # Filter out the '?' to find similar rows based on inputs
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Create a temporary row with estimated inputs for distance calculation
    # We use the average of the whole dataset for the missing goal columns
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    estimated_row = list(row)
    for g_idx in goal_indices:
        avg_val = sum(r[g_idx] for r in rows) / len(rows)
        estimated_row[g_idx] = avg_val
        
    # Find similar rows
    similar_indices = find_similar(header, rows, estimated_row, k=10)
    
    # 2. Calculate the score of the provided row using the average of similar setups
    for g_idx in goal_indices:
        avg_val = sum(rows[i][g_idx] for i in similar_indices) / len(similar_indices)
        estimated_row[g_idx] = avg_val
        
    target_score = get_score(header, estimated_row)
    
    # 3. Calculate percentile rank
    better_count = 0
    for r in rows:
        if get_score(header, r) < target_score:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This setup is outperformed by {p:.1%} of historical configurations, suggesting that other options provide better trade-offs between cost and performance."
    
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
        
        # Example: Compare a specific row (index 50) as "Setup B"
        test_row = list(rows[50])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        print(f"Customer Inquiry: I liked setup B. You recommended A. Explain why not B.")
        print(f"Answer: {reason}")
        print(f"Performance Rank: {p:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
