import csv

def flow(header, row, seen):
    """
    Returns True if the current row is 'bad' compared to the history.
    We define 'bad' as a significant degradation in performance compared 
    to the best seen so far.
    """
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        s = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            s += val if op == '-' else -val
        return s

    if not seen:
        return False
    
    # Calculate the best score seen so far
    best_score = min(get_score(r) for r in seen)
    current_score = get_score(row)
    
    # If the current score is significantly worse than the best (e.g., 20% worse),
    # we flag it as "going bad".
    # We use a threshold to avoid noise.
    if current_score > best_score * 1.2:
        return True
    
    return False

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        seen = []
        alerts = 0
        for row in rows:
            if flow(header, row, seen):
                alerts += 1
            seen.append(row)
            
        print(f"Monitoring complete. {alerts} instances of performance degradation detected.")
        print("The system is configured to alert when new results perform 20% worse than the historical best.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
