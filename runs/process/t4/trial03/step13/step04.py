import csv
import pandas as pd
import numpy as np
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    the current best seen so far.
    """
    if not seen:
        return True
    
    # Combine current row and seen rows to normalize goals
    all_rows = seen + [row]
    df = pd.DataFrame(all_rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals
    scores = []
    for col in goals:
        vals = df[col].astype(float)
        # Handle division by zero if all values are the same
        rng = vals.max() - vals.min()
        norm = (vals - vals.min()) / rng if rng > 0 else 0
        if col.endswith('-'):
            scores.append(1 - norm)
        else:
            scores.append(norm)
    
    combined_scores = np.mean(scores, axis=0)
    
    # If the current row's score is the best seen so far, accept it
    return combined_scores[-1] >= np.max(combined_scores[:-1])

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        accepted = []
        seen = []
        for row in rows:
            if flow(header, row, seen):
                accepted.append(row)
            seen.append(row)
            
        print(f"Customer Inquiry: Sequential Approval Process")
        print(f"Total proposals reviewed: {len(rows)}")
        print(f"Total proposals approved: {len(accepted)}")
        print("Strategy: Approved if the proposal is better than all previous ones.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
