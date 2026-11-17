import pandas as pd
import numpy as np

def remember(header, rows):
    """
    Identifies rows that perform well on all goals.
    Goals ending in '-' are minimized, '+' are maximized.
    We use a simple Pareto-based approach: normalize goals to [0, 1]
    and pick rows with the lowest aggregate distance to the ideal point.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals to [0, 1]
    normalized = df[goals].copy()
    for col in goals:
        col_min = normalized[col].min()
        col_max = normalized[col].max()
        if col.endswith('-'):
            # Minimize: 0 is best, 1 is worst
            normalized[col] = (normalized[col] - col_min) / (col_max - col_min + 1e-9)
        else:
            # Maximize: 1 is best, 0 is worst
            normalized[col] = (col_max - normalized[col]) / (col_max - col_min + 1e-9)
            
    # Calculate aggregate score (sum of normalized distances to ideal)
    # Lower is better
    df['score'] = normalized.sum(axis=1)
    
    # Select top 5% or at least 1
    n_select = max(1, int(len(df) * 0.05))
    best_indices = df['score'].nsmallest(n_select).index.tolist()
    
    return best_indices

if __name__ == "__main__":
    import csv
    
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            # Convert numeric columns to float, keep symbolic as is
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    indices = remember(header, rows)
    
    print(f"Found {len(indices)} rows that performed unusually well.")
    print("Indices of best rows:", indices)
    
    # Print a sample of the best rows
    print("\nSample of best rows:")
    for idx in indices[:5]:
        print(f"Row {idx}: {rows[idx]}")
