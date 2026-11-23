import csv
import pandas as pd
import numpy as np

def remember(header, rows):
    """
    Identifies rows that perform well across all goal columns.
    Goals ending in '-' are minimized, goals ending in '+' are maximized.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals to a [0, 1] scale where 1 is always "best"
    normalized_goals = pd.DataFrame(index=df.index)
    for goal in goals:
        col = df[goal].astype(float)
        if goal.endswith('-'):
            # Lower is better: (max - x) / (max - min)
            normalized_goals[goal] = (col.max() - col) / (col.max() - col.min())
        else:
            # Higher is better: (x - min) / (max - min)
            normalized_goals[goal] = (col - col.min()) / (col.max() - col.min())
            
    # Calculate a composite score (average of normalized goals)
    # We want rows that are consistently good across all goals
    df['composite'] = normalized_goals.mean(axis=1)
    
    # Select top 5% (or at least 1)
    n_rows = len(df)
    k = max(1, int(n_rows * 0.05))
    
    best_indices = df['composite'].nlargest(k).index.tolist()
    return sorted(best_indices)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to floats
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        indices = remember(header, rows)
        
        print(f"Found {len(indices)} top-performing setups.")
        print("Indices of the best rows:")
        print(indices)
        
        # Print a summary of the first best row found
        best_row = rows[indices[0]]
        print(f"\nExample of a top-performing row (index {indices[0]}):")
        for h, v in zip(header, best_row):
            print(f"  {h}: {v}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
