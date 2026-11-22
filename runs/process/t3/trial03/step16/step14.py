import csv

def flow(header, row, seen):
    """
    Returns True if the current row is 'bad' (a performance drop),
    signaling the customer to stop.
    
    A row is 'bad' if its aggregate performance is significantly worse 
    than the average of the previously seen rows.
    """
    if not seen:
        return False

    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        scores = []
        for i in goal_indices:
            val = r[i]
            # Normalize: '-' minimized (1-val), '+' maximized (val)
            # Since data is [0,1], we use raw values as normalized proxies
            if header[i].endswith('-'):
                scores.append(1.0 - val)
            else:
                scores.append(val)
        return sum(scores) / len(scores)

    # Calculate average score of all seen rows
    seen_scores = [get_score(r) for r in seen]
    avg_seen = sum(seen_scores) / len(seen_scores)
    
    # Calculate current row score
    current_score = get_score(row)
    
    # If current performance drops significantly below the average (e.g., 2 standard deviations)
    # or simply below the average, we flag it as 'going bad'.
    # Using a threshold of 0.85 * average to be sensitive to degradation.
    if current_score < (0.85 * avg_seen):
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
        alerted = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"ALERT: Performance degradation detected at row {i+1}.")
                alerted = True
                break
            seen.append(row)
            
        if not alerted:
            print("Monitoring complete: No significant performance degradation detected.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
