import csv

def flow(header, row, seen):
    """
    Detects if the performance of incoming rows is starting to 'go bad'.
    We maintain a moving average of the performance of the last 20 rows.
    If the current row's score is significantly worse (e.g., > 2 standard 
    deviations) than the recent moving average, we return True to warn the user.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]

    def get_score(r):
        s = 0
        for i in goal_indices:
            val = float(r[i])
            s += val if header[i].endswith('-') else (1.0 - val)
        return s

    if len(seen) < 20:
        return False

    # Calculate scores of recent history
    recent_scores = [get_score(r) for r in seen[-20:]]
    avg = sum(recent_scores) / len(recent_scores)
    var = sum((x - avg) ** 2 for x in recent_scores) / len(recent_scores)
    std = var ** 0.5

    # If current row is significantly worse than the recent average
    current_score = get_score(row)
    if current_score > (avg + 2 * std):
        return True
    
    return False

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        seen = []
        warnings = 0
        for row in rows:
            if flow(header, row, seen):
                warnings += 1
            seen.append(row)
            
        print(f"Analysis complete. Processed {len(rows)} rows.")
        if warnings > 0:
            print(f"Warning: Detected {warnings} instances where performance degraded significantly.")
            print("The system identified setups that performed worse than the recent moving average.")
        else:
            print("Performance remains stable; no significant degradation detected.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
