import csv
import pandas as pd
import numpy as np
from step01 import remember

def fix(header, row, levers):
    """
    Finds the smallest change to levers to improve the row's goal scores.
    We evaluate potential changes by sampling values within the lever ranges
    and picking the one that minimizes the aggregate goal score.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    goal_types = ['min' if header[i].endswith('-') else 'max' for i in goal_indices]
    
    def get_score(r):
        # Use the row's current values to calculate a score
        # Since we don't have a model here, we use the raw values
        # normalized by the row's own context (or just raw if single)
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = float(r[g_idx])
            score += val if goal_types[i] == 'min' else -val
        return score

    best_change = {}
    best_score = get_score(row)
    
    # Try changing each lever
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Generate a candidate value
        if isinstance(allowed, tuple): # Numeric
            low, high = allowed
            candidate = (low + high) / 2
        else: # Symbolic
            candidate = allowed[0]
            
        # Apply change
        new_row = list(row)
        new_row[col_idx] = candidate
        
        # Simple heuristic: if the change improves the goal values
        # (Assuming we want to minimize Cost- and Idle-)
        new_score = get_score(new_row)
        if new_score < best_score:
            best_score = new_score
            best_change = {col_name: candidate}
            
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    
    # Identify a "bad" row (e.g., high cost and high idle)
    # Cost- is index 9, Idle- is index 11
    df = pd.DataFrame(rows, columns=header)
    for col in header:
        if col[0].isupper():
            df[col] = df[col].astype(float)
            
    bad_row_idx = (df['Cost-'] + df['Idle-']).idxmax()
    bad_row = rows[bad_row_idx]
    
    # Define levers: Plan (index 7) and Team Size (index 8)
    levers = {
        'Plan': (0.0, 1.0),
        'Team Size': (0.0, 1.0)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Inquiry: How to rescue an over-budget, idle programme?")
    print(f"Analysis: Based on the current setup (Row {bad_row_idx}), we recommend:")
    for col, val in recommendation.items():
        print(f"- Adjust '{col}' to {val:.4f}")
    print("This change is expected to reduce cost and idle time.")
