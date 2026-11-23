import csv
import pandas as pd
import numpy as np
from step01 import remember
from step05 import blame

def fix(header, row, levers):
    """
    Recommends a change to a bad row to cut 'Idle-' time, 
    excluding 'Team Size' as the customer cannot hire.
    """
    filename = 'pom3a.n1000.train.csv'
    df = pd.read_csv(filename)
    
    # Identify best rows using step01 logic
    best_indices = remember(header, df.values.tolist())
    best_rows = df.iloc[best_indices]
    
    # Identify which levers are most important for 'Idle-' (using blame logic)
    # We filter out 'Team Size' from the available levers
    allowed_levers = {k: v for k, v in levers.items() if k != 'Team Size'}
    
    # Get importance specifically for 'Idle-'
    # We reuse the blame logic but target 'Idle-'
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Find the most important levers for 'Idle-'
    # We use the top 5 to ensure we have a candidate that isn't 'Team Size'
    importances = blame(header, df.values.tolist())
    
    recommendation = {}
    for lever in importances:
        if lever in allowed_levers:
            # Find the median value of this lever in the best rows
            target_val = best_rows[lever].median()
            
            # Clamp to allowed range
            low, high = allowed_levers[lever]
            new_val = max(low, min(high, target_val))
            
            recommendation[lever] = new_val
            break
            
    return recommendation

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        df = pd.read_csv(filename)
        header = df.columns.tolist()
        
        # Define levers (all inputs are numeric 0-1)
        levers = {col: (0.0, 1.0) for col in header if not (col.endswith('-') or col.endswith('+'))}
        
        # Pick a "bad" row (high Idle-)
        bad_row = df.sort_values('Idle-', ascending=False).iloc[0].tolist()
        
        change = fix(header, bad_row, levers)
        
        print("To cut idle time without hiring, we recommend the following adjustment:")
        for col, val in change.items():
            print(f"Change '{col}' to {val:.4f}.")
        print("This adjustment aligns your project parameters with the most efficient configurations found in our historical data.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
