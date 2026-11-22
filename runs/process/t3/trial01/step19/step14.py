import csv

def flow(header, row, seen):
    """
    Detects if the incoming stream of rows has started to 'go bad'.
    We compare the current row's performance against the historical 
    performance baseline (the mean of all previously seen rows).
    If the current row's performance drops significantly below the 
    moving average, we return True to signal a warning.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        score = 0
        for i in goal_indices:
            val = r[i]
            # Normalize: lower is better for '-', higher for '+'
            # Since we don't have global min/max, we use 0-1 range
            if header[i].endswith('-'):
                score += (1.0 - val)
            else:
                score += val
        return score / len(goal_indices)

    # Need a baseline to compare against
    if len(seen) < 10:
        return False
    
    # Calculate moving average of performance
    scores = [get_score(r) for r in seen]
    avg_score = sum(scores) / len(scores)
    curr_score = get_score(row)
    
    # If current performance is significantly worse than the average 
    # (e.g., 2 standard deviations below mean), signal a warning.
    # Here we use a simpler threshold: 20% drop from the average.
    if curr_score < (avg_score * 0.8):
        return True
        
    return False

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
        warning_triggered = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Warning: Performance degradation detected at row {i}!")
                warning_triggered = True
                break
            seen.append(row)
            
        if not warning_triggered:
            print("No significant performance degradation detected in the stream.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
