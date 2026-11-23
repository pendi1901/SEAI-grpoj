import csv

def flow(header, row, seen):
    """
    Decides whether to accept a row based on the Secretary Problem logic.
    We observe a sample to establish a baseline (the 'best' seen so far),
    then accept the first row that is better than that baseline.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score(r):
        # Lower is better: minimize '-' and maximize '+' (by inverting)
        s = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            s += val if op == '-' else (1.0 - val)
        return s

    # If this is the first row, we can't compare it to anything
    if not seen:
        return False

    # Calculate the best score seen so far
    best_seen = min(score(r) for r in seen)

    # If we have seen enough (e.g., 20% of data), start accepting
    # If the current row is better than anything seen before, accept it.
    # Otherwise, keep looking.
    if len(seen) > (800 * 0.2):
        if score(row) < best_seen:
            return True
            
    return False

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [ [float(x) for x in row] for row in reader ]
        
        seen = []
        accepted = None
        for row in rows:
            if flow(header, row, seen):
                accepted = row
                break
            seen.append(row)
        
        if accepted:
            print("Decision: Approved the current configuration.")
            print(f"Accepted row data: {accepted}")
        else:
            print("Decision: No suitable configuration found in the stream.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
