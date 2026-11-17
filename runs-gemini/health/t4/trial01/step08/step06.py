import csv
import pandas as pd
import numpy as np
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Returns (p, reason) where p is the fraction of rows that 'row' is better than,
    and reason is a human-readable explanation.
    """
    # 1. Fill in the missing goals for the candidate row
    # We use the guess function from step02, but we need to pass it the full dataset
    # to train the model.
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Prepare training data (rows with goals) and test data (the candidate row)
    train_data = [r for r in rows]
    test_data = [row]
    
    # Predict the missing goals
    predicted_goals = guess(header, train_data, test_data)
    
    # Create a full version of the candidate row
    full_row = list(row)
    for i, goal_idx in enumerate(goal_indices):
        full_row[goal_idx] = predicted_goals[i]
        
    # 2. Compare against all rows
    # Use the scoring logic from step01
    all_data = rows + [full_row]
    df = pd.DataFrame(all_data, columns=header)
    
    min_cols = [c for c in header if c.endswith('-')]
    max_cols = [c for c in header if c.endswith('+')]
    
    scores = pd.DataFrame(index=df.index)
    for col in min_cols:
        col_min, col_max = df[col].min(), df[col].max()
        scores[col] = (col_max - df[col]) / (col_max - col_min + 1e-9)
    for col in max_cols:
        col_min, col_max = df[col].min(), df[col].max()
        scores[col] = (df[col] - col_min) / (col_max - col_min + 1e-9)
        
    total_scores = scores.sum(axis=1)
    candidate_score = total_scores.iloc[-1]
    other_scores = total_scores.iloc[:-1]
    
    # 3. Calculate fraction
    better_than = (other_scores < candidate_score).sum()
    p = better_than / len(other_scores)
    
    reason = f"This configuration outperforms {p:.1%} of all known setups based on a multi-objective analysis of error and performance metrics."
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row]
            data.append(processed_row)
            
    # Pick a sample row to justify
    sample_row = list(data[0])
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    for idx in goal_indices:
        sample_row[idx] = "?"
        
    p, reason = justify(header, data, sample_row)
    print(f"Justification score: {p:.4f}")
    print(f"Reason: {reason}")
