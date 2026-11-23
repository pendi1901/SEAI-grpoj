import csv
import pandas as pd
import numpy as np

def remember(header, rows):
    """
    Identifies rows that perform well across all goal columns.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [col for col in header if col.endswith(('-', '+'))]
    
    # Normalize goals to [0, 1] range for comparison
    # For '-', lower is better (1 - normalized value)
    # For '+', higher is better (normalized value)
    scores = pd.DataFrame(index=df.index)
    for goal in goals:
        col_data = df[goal].astype(float)
        normalized = (col_data - col_data.min()) / (col_data.max() - col_data.min())
        if goal.endswith('-'):
            scores[goal] = 1 - normalized
        else:
            scores[goal] = normalized
            
    # Calculate aggregate score (mean of normalized goals)
    df['aggregate'] = scores.mean(axis=1)
    
    # Select top 5% (or at least 1)
    n_rows = len(df)
    k = max(1, int(n_rows * 0.05))
    
    best_indices = df['aggregate'].nlargest(k).index.tolist()
    return sorted(best_indices)

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
        
        print(f"Analysis complete. Found {len(best_indices)} top-performing setups.")
        print("Indices of the best rows (0-based):")
        print(best_indices)
        
        # Print a summary of the first best row found
        if best_indices:
            print("\nDetails of the top-ranked setup:")
            best_row = rows[best_indices[0]]
            for h, v in zip(header, best_row):
                print(f"  {h}: {v}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
