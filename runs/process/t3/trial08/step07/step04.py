import csv
import pandas as pd

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    the best row seen so far. Uses a simple threshold strategy:
    accept if the row is in the top 5% of the current distribution.
    """
    if not seen:
        return True

    # Identify goal columns
    goals = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(r):
        # Calculate a simple normalized score for the row
        # We don't have the full distribution, so we compare against 'seen'
        # For this online task, we evaluate if the row is better than the current best
        score = 0
        for i in goals:
            val = float(r[i])
            # Simple heuristic: minimize '-' (lower is better), maximize '+' (higher is better)
            if header[i].endswith('-'):
                score -= val
            else:
                score += val
        return score

    current_score = get_score(row)
    seen_scores = [get_score(s) for s in seen]
    
    # If this row is better than the best seen so far, accept it
    if current_score >= max(seen_scores):
        return True
    
    # Otherwise, accept with a small probability (exploration)
    return False

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
                rows.append(processed_row)
        
        accepted = []
        seen = []
        for row in rows:
            if flow(header, row, seen):
                accepted.append(row)
            seen.append(row)
            
        print(f"Decision Process Complete.")
        print(f"Total proposals reviewed: {len(rows)}")
        print(f"Total proposals accepted: {len(accepted)}")
        print("Strategy: Accepted proposals that outperformed all previous records.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
