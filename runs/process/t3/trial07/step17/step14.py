import csv

def flow(header, row, seen):
    """
    Warns the customer if a new row is significantly worse than the 
    historical baseline. We define 'bad' as being in the bottom 10% 
    of performance compared to all previously seen data.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    def get_score(r):
        # Calculate normalized score for a row based on seen data
        scores = []
        for i in goal_indices:
            col_vals = [s[i] for s in seen] + [r[i]]
            min_v, max_v = min(col_vals), max(col_vals)
            norm = (r[i] - min_v) / (max_v - min_v + 1e-9)
            scores.append(1 - norm if header[i].endswith('-') else norm)
        return sum(scores) / len(scores)

    # Need a baseline before we can warn
    if len(seen) < 50:
        return False
    
    # Calculate scores for all seen rows
    seen_scores = [get_score(s) for s in seen]
    current_score = get_score(row)
    
    # Threshold: if current row is worse than 90% of history, warn (return True)
    threshold = sorted(seen_scores)[int(len(seen_scores) * 0.1)]
    
    return current_score < threshold

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
        for row in rows:
            if flow(header, row, seen):
                warnings += 1
            seen.append(row)
            
        print("Customer Inquiry: Warn me the moment a result starts to go bad.")
        print(f"Analysis: Monitored {len(rows)} incoming results.")
        print(f"Warning: Detected {warnings} instances where performance dropped significantly below historical norms.")
        print("Conclusion: We recommend reviewing the process parameters for these flagged setups.")
        exit(0)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
