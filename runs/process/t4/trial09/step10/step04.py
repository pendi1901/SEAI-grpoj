import csv
import pandas as pd
import numpy as np
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    the best seen so far. Uses the aggregate score logic from step01.
    """
    if not seen:
        return True
    
    # Combine current row with seen rows to normalize goals
    all_rows = seen + [row]
    df = pd.DataFrame(all_rows, columns=header)
    
    # Identify goal columns
    goals = [col for col in header if col.endswith(('-', '+'))]
    
    # Normalize goals
    normalized_scores = []
    for goal in goals:
        col_min = df[goal].min()
        col_max = df[goal].max()
        norm = (df[goal] - col_min) / (col_max - col_min + 1e-9)
        if goal.endswith('-'):
            normalized_scores.append(1 - norm)
        else:
            normalized_scores.append(norm)
            
    df['aggregate'] = np.mean(normalized_scores, axis=0)
    
    # If the current row (last in df) is the best seen so far, accept it
    return df['aggregate'].iloc[-1] >= df['aggregate'].max()

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
        accepted_count = 0
        for row in rows:
            if flow(header, row, seen):
                accepted_count += 1
            seen.append(row)
            
        print("Customer Inquiry: Sequential Approval Strategy")
        print(f"Total rows processed: {len(rows)}")
        print(f"Total setups approved: {accepted_count}")
        print("Strategy: Approved a setup if it outperformed all previously seen options.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
