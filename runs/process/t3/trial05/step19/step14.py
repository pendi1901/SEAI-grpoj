import csv

def flow(header, row, seen):
    """
    Warns the customer if a new row is significantly worse than the 
    historical average performance.
    
    We define 'bad' as a row whose composite goal score is more than 
    one standard deviation below the mean of the 'seen' data.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(r):
        # Normalize goals: 1 is best, 0 is worst
        # Since we don't have the full dataset, we use 'seen' to estimate bounds
        if not seen:
            return 0
        
        scores = []
        for i in goal_indices:
            vals = [s[i] for s in seen]
            min_v, max_v = min(vals), max(vals)
            rng = max_v - min_v
            if rng == 0:
                scores.append(0.5)
            else:
                norm = (r[i] - min_v) / rng
                scores.append(1 - norm if header[i].endswith('-') else norm)
        return sum(scores) / len(scores)

    if len(seen) < 10:
        return False

    # Calculate historical performance
    historical_scores = [get_score(s) for s in seen]
    mean_score = sum(historical_scores) / len(historical_scores)
    std_score = (sum((x - mean_score)**2 for x in historical_scores) / len(historical_scores))**0.5
    
    # If current row is significantly worse than average (e.g., > 1 std dev below)
    current_score = get_score(row)
    return current_score < (mean_score - std_score)

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
        warnings = 0
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                warnings += 1
                if warnings <= 5:
                    print(f"Warning: Row {i} is performing significantly worse than historical trends.")
            seen.append(row)
            
        print(f"Analysis complete. Total warnings issued: {warnings}.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
