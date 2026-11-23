import csv
import pandas as pd
import numpy as np
from step01 import remember

def flow(header, row, seen):
    """
    Warns the user if the performance of incoming rows starts to degrade.
    We compare the current row's aggregate score against the moving average
    of the last 20% of seen rows. If the current row is significantly worse
    than the recent trend, we return True (triggering a warning/stop).
    """
    if len(seen) < 20:
        return False

    # Combine seen and current row to calculate normalized scores
    all_rows = seen + [row]
    df = pd.DataFrame(all_rows, columns=header)
    
    goals = [col for col in header if col.endswith(('-', '+'))]
    scores = pd.DataFrame(index=df.index)
    for goal in goals:
        col_data = df[goal].astype(float)
        min_val, max_val = col_data.min(), col_data.max()
        norm = (col_data - min_val) / (max_val - min_val + 1e-9)
        scores[goal] = 1 - norm if goal.endswith('-') else norm
    
    df['agg'] = scores.mean(axis=1)
    
    # Define recent trend (last 20% of seen)
    window = max(5, len(seen) // 5)
    recent_avg = df['agg'].iloc[-window-1:-1].mean()
    current_score = df['agg'].iloc[-1]
    
    # If current performance drops significantly below the recent average
    # (e.g., more than 1 standard deviation below), warn the user.
    std_dev = df['agg'].iloc[-window-1:-1].std() or 0.1
    return current_score < (recent_avg - std_dev)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        seen = []
        warning_triggered = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Warning: Performance degradation detected at row {i}!")
                warning_triggered = True
                break
            seen.append(row)
            
        if not warning_triggered:
            print("Monitoring complete: No significant performance degradation detected.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
