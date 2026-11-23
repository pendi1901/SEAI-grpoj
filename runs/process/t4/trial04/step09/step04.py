import csv
import pandas as pd
import numpy as np
from step01 import remember

def flow(header, row, seen):
    """
    Implements the Secretary Problem logic:
    1. Observe a sample (37% of total) to establish a baseline of 'good' performance.
    2. After the sample, accept the first row that is better than the best seen so far.
    """
    # Identify goal columns
    goals = [col for col in header if col.endswith(('-', '+'))]
    
    # If this is the first row, we can't compare yet
    if not seen:
        return False
    
    # Calculate a simple score for a row (normalized distance to ideal)
    # Since we don't have the full dataset min/max, we use the 'seen' data as context
    all_rows = seen + [row]
    df = pd.DataFrame(all_rows, columns=header)
    
    scores = pd.DataFrame(index=df.index)
    for goal in goals:
        col_min, col_max = df[goal].min(), df[goal].max()
        # Avoid division by zero
        rng = col_max - col_min if col_max != col_min else 1.0
        norm = (df[goal] - col_min) / rng
        scores[goal] = (1 - norm) if goal.endswith('-') else norm
    
    final_scores = scores.prod(axis=1)
    
    # Secretary Problem threshold: 1/e ≈ 0.37
    sample_size = int(len(all_rows) * 0.37)
    
    if len(seen) < sample_size:
        return False
    
    # Accept if current row is the best seen so far
    return final_scores.iloc[-1] >= final_scores.iloc[:-1].max()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        seen = []
        accepted = None
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                accepted = (i, row)
                break
            seen.append(row)
            
        print("Customer Inquiry: Decision on incoming proposals.")
        if accepted:
            print(f"  Approved proposal at index {accepted[0]}.")
            print(f"  Row data: {accepted[1]}")
        else:
            print("  No proposal met the criteria for approval.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
