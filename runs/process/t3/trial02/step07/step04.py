import csv
import pandas as pd
import numpy as np

def flow(header, row, seen):
    """
    Decides whether to accept a row based on the Secretary Problem logic 
    combined with a Pareto-based quality threshold.
    """
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # If it's the first row, we don't have enough info to compare
    if not seen:
        return False
    
    # Calculate a simple score for the current row
    # Lower is better: normalize goals to [0, 1] relative to seen data
    df_seen = pd.DataFrame(seen, columns=header)
    
    def get_score(r):
        score = 0
        for g in goals:
            col = df_seen[g].astype(float)
            val = float(r[header.index(g)])
            norm = (val - col.min()) / (col.max() - col.min() + 1e-9)
            if g.endswith('+'):
                norm = 1 - norm
            score += norm
        return score

    # Strategy: Accept if the current row is better than the best seen so far
    # and we have passed the initial exploration phase (e.g., 20% of data)
    current_score = get_score(row)
    best_seen_score = min([get_score(s) for s in seen])
    
    # Exploration phase: 20% of the expected 800 rows (160 rows)
    if len(seen) < 160:
        return False
    
    # If current row is better than anything seen before, accept it
    return current_score < best_seen_score

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row])
        
        accepted_count = 0
        seen = []
        for row in rows:
            if flow(header, row, seen):
                accepted_count += 1
            seen.append(row)
            
        print(f"Processed {len(rows)} proposals.")
        print(f"Accepted {accepted_count} proposals based on the decision strategy.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
