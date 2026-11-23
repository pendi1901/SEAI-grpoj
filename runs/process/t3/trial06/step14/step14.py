import csv

def get_score(header, row):
    """Calculates a normalized score [0, 1] for a row based on goals."""
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    scores = []
    for i in goal_indices:
        val = row[i]
        # Since data is normalized [0,1], we treat 1 as best
        if header[i].endswith('-'):
            scores.append(1.0 - val)
        else:
            scores.append(val)
    return sum(scores) / len(scores)

def flow(header, row, seen):
    """
    Detects if the incoming stream of data is 'going bad'.
    We compare the current row's performance against the moving average
    of the last 50 rows. If the current performance drops significantly
    below the recent trend, we flag it (return True).
    """
    if len(seen) < 50:
        return False
    
    # Calculate performance of the current row
    current_score = get_score(header, row)
    
    # Calculate moving average of the last 50 rows
    recent_scores = [get_score(header, r) for r in seen[-50:]]
    avg_recent = sum(recent_scores) / len(recent_scores)
    
    # If the current score is significantly lower than the recent average
    # (e.g., 2 standard deviations or a fixed threshold), it's 'going bad'.
    # Here we use a threshold of 0.15 drop from the moving average.
    if current_score < (avg_recent - 0.15):
        return True
    
    return False

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        seen = []
        alerts = 0
        for row in rows:
            if flow(header, row, seen):
                alerts += 1
            seen.append(row)
            
        print("Customer Report: Performance Monitoring")
        if alerts > 0:
            print(f"Warning: Detected {alerts} instances where performance dropped significantly.")
            print("The system is showing signs of instability or degradation.")
        else:
            print("Status: Performance remains stable. No significant degradation detected.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
