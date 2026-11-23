import csv
import pandas as pd
import numpy as np
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    the best seen so far. We use the aggregate scoring logic from step01.
    """
    if not seen:
        return True
    
    # Combine seen rows and current row to calculate relative performance
    all_data = seen + [row]
    df = pd.DataFrame(all_data, columns=header)
    
    # Identify goal columns
    goals = [col for col in header if col.endswith(('-', '+'))]
    
    # Normalize goals
    scores = pd.DataFrame(index=df.index)
    for goal in goals:
        col_data = df[goal].astype(float)
        # Handle case where all values are identical
        diff = col_data.max() - col_data.min()
        normalized = (col_data - col_data.min()) / diff if diff != 0 else 0
        
        if goal.endswith('-'):
            scores[goal] = 1 - normalized
        else:
            scores[goal] = normalized
            
    # Calculate aggregate scores
    df['aggregate'] = scores.mean(axis=1)
    
    # Accept if the current row is the best seen so far
    return df['aggregate'].iloc[-1] >= df['aggregate'].iloc[:-1].max()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
            
        seen = []
        accepted_count = 0
        for row in rows:
            if flow(header, row, seen):
                accepted_count += 1
            seen.append(row)
            
        print(f"Processed {len(rows)} proposals.")
        print(f"Approved {accepted_count} proposals based on real-time performance evaluation.")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
