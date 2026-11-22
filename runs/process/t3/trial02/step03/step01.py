import csv
import pandas as pd
import numpy as np

def remember(header, rows):
    """
    Identifies rows that perform well across all goal columns.
    Goals ending in '-' are minimized, goals ending in '+' are maximized.
    We normalize the goals and find the Pareto front or simply 
    the rows with the lowest aggregate normalized cost.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals to [0, 1] range
    normalized_goals = pd.DataFrame(index=df.index)
    for goal in goals:
        col = df[goal].astype(float)
        if goal.endswith('-'):
            # Minimize: lower is better (0 is best)
            normalized_goals[goal] = (col - col.min()) / (col.max() - col.min() + 1e-9)
        else:
            # Maximize: higher is better (0 is best after inversion)
            normalized_goals[goal] = (col.max() - col) / (col.max() - col.min() + 1e-9)
            
    # Calculate aggregate score (sum of normalized goals)
    # Lower aggregate score is better
    df['score'] = normalized_goals.sum(axis=1)
    
    # Select the top 5% (or at least one)
    n_rows = len(df)
    k = max(1, n_rows // 20)
    
    best_indices = df.nsmallest(k, 'score').index.tolist()
    return best_indices

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
        
        print(f"Found {len(best_indices)} rows that performed unusually well.")
        print("Indices of best rows:", best_indices)
        
        # Display a summary of the best rows
        df = pd.DataFrame(rows, columns=header)
        print("\nSummary of best rows:")
        print(df.iloc[best_indices])
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
