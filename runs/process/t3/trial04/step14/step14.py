import csv

def flow(header, row, seen):
    """
    Warns the user if the current row is significantly worse than the 
    historical baseline (the 'seen' data).
    
    Strategy:
    1. Calculate a normalized score for the current row and all seen rows.
    2. If the current row's score is significantly lower (e.g., 2 standard 
       deviations below the mean of seen rows), return True to flag it as 'bad'.
    """
    if not seen:
        return False

    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(r):
        scores = []
        for i in goal_indices:
            col_vals = [s[i] for s in seen + [r]]
            c_min, c_max = min(col_vals), max(col_vals)
            rng = c_max - c_min + 1e-9
            norm = (r[i] - c_min) / rng
            scores.append(1 - norm if header[i].endswith('-') else norm)
        return sum(scores) / len(scores)

    # Calculate scores for all seen rows
    seen_scores = [get_score(s) for s in seen]
    current_score = get_score(row)
    
    # Calculate mean and standard deviation of seen performance
    mean_score = sum(seen_scores) / len(seen_scores)
    variance = sum((s - mean_score)**2 for s in seen_scores) / len(seen_scores)
    stdev = variance**0.5
    
    # Flag as 'bad' if it is more than 1.5 standard deviations below the mean
    # (This threshold is sensitive enough to catch performance degradation)
    if current_score < (mean_score - 1.5 * stdev):
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
        alerts = 0
        for row in rows:
            if flow(header, row, seen):
                alerts += 1
            seen.append(row)
            
        print("Performance Monitoring Analysis:")
        print(f"Processed {len(rows)} project updates.")
        print(f"Detected {alerts} instances where project performance degraded significantly.")
        print("The system is configured to alert you immediately when a new setup")
        print("falls statistically below the established historical baseline.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
