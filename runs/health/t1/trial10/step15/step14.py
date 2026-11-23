import csv

def flow(header, row, seen):
    """
    Decides if the current row is the best seen so far.
    We stop if the current row's multi-objective score is the best 
    among all rows seen so far, and we have seen at least 50 rows 
    to ensure the baseline is stable.
    """
    if not seen:
        return False
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(r):
        scores = []
        for idx in goal_indices:
            # We normalize based on the current 'seen' set to evaluate relative quality
            vals = [s[idx] for s in seen + [r]]
            mn, mx = min(vals), max(vals)
            norm = (r[idx] - mn) / (mx - mn) if mx > mn else 0
            scores.append(1.0 - norm if header[idx].endswith('-') else norm)
        return sum(scores) / len(scores)

    # Only stop if we have a reasonable sample size
    if len(seen) < 50:
        return False

    current_score = get_score(row)
    seen_scores = [get_score(s) for s in seen]
    
    # Stop if this is the best score encountered so far
    return current_score >= max(seen_scores)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)

        seen = []
        stopped = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Stopped at row {i+1}: Found a new best configuration.")
                stopped = True
                break
            seen.append(row)
        
        if not stopped:
            print("Finished all runs without finding a significant improvement plateau.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
