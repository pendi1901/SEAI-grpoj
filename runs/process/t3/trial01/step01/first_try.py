import csv
import pandas as pd
import numpy as np

def remember(header, rows):
    """
    Identifies rows that perform well across all goal columns.
    Goals ending in '-' are minimized, goals ending in '+' are maximized.
    We use a simple Pareto-based approach or normalization to find the best rows.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals to [0, 1] range
    # For '-', lower is better (1 - normalized_value)
    # For '+', higher is better (normalized_value)
    scores = pd.DataFrame(index=df.index)
    for goal in goals:
        col = df[goal].astype(float)
        norm = (col - col.min()) / (col.max() - col.min())
        if goal.endswith('-'):
            scores[goal] = 1 - norm
        else:
            scores[goal] = norm
            
    # Aggregate score (mean of normalized goals)
    df['combined_score'] = scores.mean(axis=1)
    
    # Select top 5% (or at least one)
    n_rows = len(df)
    k = max(1, int(n_rows * 0.05))
    
    top_indices = df['combined_score'].nlargest(k).index.tolist()
    return sorted(top_indices)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float, keep symbolic as is
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print(f"Found {len(best_indices)} top-performing setups.")
        print("Indices of the best rows (0-based):")
        print(best_indices)
        
        # Display a summary of the best rows
        print("\nSummary of best rows:")
        goals = [c for c in header if c.endswith('-') or c.endswith('+')]
        for idx in best_indices:
            goal_vals = {g: rows[idx][header.index(g)] for g in goals}
            print(f"Row {idx}: {goal_vals}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
