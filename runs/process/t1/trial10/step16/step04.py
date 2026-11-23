import csv

def flow(header, row, seen):
    """
    Implements the Secretary Problem logic with a threshold.
    We observe the first 20% of rows to establish a baseline 'best' 
    and then accept the first row that beats that baseline.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def get_score(r):
        s = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            if op == '+':
                s += (1.0 - val)
            else:
                s += val
        return s

    # If we have seen nothing, we cannot decide based on history
    if not seen:
        return False

    # Calculate the best score seen so far
    best_score = min(get_score(r) for r in seen)
    
    # If we have seen enough (e.g., 20% of expected 800 rows), 
    # start accepting if current is better than anything seen before.
    if len(seen) > 160:
        if get_score(row) < best_score:
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
        accepted = None
        for row in rows:
            if flow(header, row, seen):
                accepted = row
                break
            seen.append(row)
            
        if accepted:
            print("Decision: Approved the current proposal.")
            print(f"Accepted row: {accepted}")
        else:
            print("Decision: No proposal met the criteria.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
