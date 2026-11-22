import csv
import pandas as pd
from step01 import remember

def flow(header, row, seen):
    """
    Returns True if the current row is significantly worse than the 
    historical performance, signaling that the process is 'going bad'.
    We define 'going bad' as the current row having an aggregate score 
    worse than the 95th percentile of all previously seen rows.
    """
    if not seen:
        return False
    
    # Combine seen rows and current row to normalize goals
    all_rows = seen + [row]
    df = pd.DataFrame(all_rows, columns=header)
    
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Calculate aggregate score (lower is better)
    normalized_goals = pd.DataFrame(index=df.index)
    for goal in goals:
        col = df[goal].astype(float)
        if goal.endswith('-'):
            normalized_goals[goal] = (col - col.min()) / (col.max() - col.min())
        else:
            normalized_goals[goal] = (col.max() - col) / (col.max() - col.min())
            
    df['score'] = normalized_goals.sum(axis=1)
    
    # If the current row (last index) has a score worse than 95% of history,
    # it is "going bad".
    current_score = df.iloc[-1]['score']
    history_scores = df['score'][:-1]
    
    # Threshold: 95th percentile of history
    threshold = history_scores.quantile(0.95)
    
    return current_score > threshold

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        alerts = 0
        seen = []
        for row in rows:
            if flow(header, row, seen):
                alerts += 1
            seen.append(row)
            
        print("Customer Inquiry: Warn me the moment a programme starts to go bad.")
        print(f"Analysis: Monitored {len(rows)} incoming programme records.")
        print(f"Alerts triggered: {alerts}.")
        print("A warning is issued when a new record's performance score exceeds the 95th percentile of historical data.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
