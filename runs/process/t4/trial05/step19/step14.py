import csv
import pandas as pd
import numpy as np
from step01 import remember

def flow(header, row, seen):
    """
    Warns the customer if the performance of the incoming row is significantly 
    worse than the historical baseline (the 20th percentile of seen rows).
    """
    if not seen:
        return False
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Convert seen rows and current row to DataFrame
    df = pd.DataFrame(seen + [row], columns=header)
    
    # Normalize goals
    norm_df = pd.DataFrame(index=df.index)
    for goal in goals:
        col = df[goal].astype(float)
        # Handle potential division by zero if all values are the same
        rng = col.max() - col.min()
        norm = (col - col.min()) / rng if rng > 0 else 0
        norm_df[goal] = (1 - norm) if goal.endswith('-') else norm
    
    scores = norm_df.prod(axis=1)
    
    # Baseline: 20th percentile of seen rows
    # If the current row's score is below this, it's "going bad"
    baseline = scores.iloc[:-1].quantile(0.2)
    current_score = scores.iloc[-1]
    
    # Return True if it's performing poorly (below the 20th percentile)
    return current_score < baseline

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        seen = []
        warnings = 0
        for row in rows:
            if flow(header, row, seen):
                warnings += 1
            seen.append(row)
            
        print("Customer Inquiry: Monitoring project performance.")
        print(f"Analysis: Processed {len(rows)} weekly updates.")
        print(f"Warning: {warnings} updates showed a significant drop in performance.")
        print("Strategy: We flag any update that falls into the bottom 20% of historical performance.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
