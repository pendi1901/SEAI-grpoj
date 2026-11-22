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
    
    # Normalize goals to [0, 1] range for comparison
    # For '-', lower is better (1 - normalized value)
    # For '+', higher is better (normalized value)
    scores = []
    for col in goals:
        vals = df[col].astype(float)
        norm = (vals - vals.min()) / (vals.max() - vals.min())
        if col.endswith('-'):
            scores.append(1 - norm)
        else:
            scores.append(norm)
    
    # Aggregate scores (mean of normalized goals)
    df['combined_score'] = np.mean(scores, axis=0)
    
    # Select top 5% (or at least 1)
    n_rows = len(df)
    k = max(1, int(n_rows * 0.05))
    
    # Get indices of the rows with the highest combined scores
    top_indices = df['combined_score'].nlargest(k).index.tolist()
    
    return top_indices

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
        print("Indices of best rows:", best_indices)
        print("\nTop 3 examples (first 3 from the list):")
        for idx in best_indices[:3]:
            print(f"Row {idx}: {rows[idx]}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
