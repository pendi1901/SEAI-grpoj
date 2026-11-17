import csv

def flow(header, row, seen):
    """
    Decides whether to stop at the current row based on a simple threshold.
    We define 'good enough' as being in the top 5% of the potential range 
    of the aggregate score based on historical data or current observations.
    """
    # Identify goal columns
    min_indices = [i for i, h in enumerate(header) if h.endswith('-')]
    max_indices = [i for i, h in enumerate(header) if h.endswith('+')]
    
    def get_score(r):
        # Calculate normalized score for a row
        # Since we don't have global min/max, we use the current row's values
        # relative to the 'seen' data distribution.
        if not seen:
            return 0.5
        
        scores = []
        for i in min_indices:
            vals = [s[i] for s in seen if isinstance(s[i], (int, float))]
            if not vals: continue
            c_min, c_max = min(vals), max(vals)
            val = r[i] if isinstance(r[i], (int, float)) else c_max
            scores.append((c_max - val) / (c_max - c_min + 1e-9) if c_max > c_min else 0)
            
        for i in max_indices:
            vals = [s[i] for s in seen if isinstance(s[i], (int, float))]
            if not vals: continue
            c_min, c_max = min(vals), max(vals)
            val = r[i] if isinstance(r[i], (int, float)) else c_min
            scores.append((val - c_min) / (c_max - c_min + 1e-9) if c_max > c_min else 0)
            
        return sum(scores) / len(scores) if scores else 0.5

    # If we have seen enough, stop if the current row is in the top 5%
    if len(seen) > 50:
        current_score = get_score(row)
        seen_scores = [get_score(s) for s in seen]
        threshold = sorted(seen_scores, reverse=True)[int(len(seen_scores) * 0.05)]
        if current_score >= threshold:
            return True
            
    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.train.csv'
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            data.append(processed_row)

    seen = []
    found = False
    for i, row in enumerate(data):
        if flow(header, row, seen):
            print(f"Stopped at row {i}: Found a setup good enough to ship.")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("Processed all rows; no setup met the strict shipping criteria.")
