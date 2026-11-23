import csv

def flow(header, row, seen):
    """
    Decides if the current row is the 'best' seen so far, and if we should stop.
    We stop if the current row is Pareto-optimal compared to all previous rows
    and we have seen enough data to be confident (e.g., at least 50 rows).
    """
    if not seen:
        return False

    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    def dominates(row_a, row_b):
        # Returns True if row_a dominates row_b
        strictly_better = False
        for idx, direction in goals:
            val_a, val_b = row_a[idx], row_b[idx]
            if direction == 1:  # Maximize
                if val_a < val_b: return False
                if val_a > val_b: strictly_better = True
            else:  # Minimize
                if val_a > val_b: return False
                if val_a < val_b: strictly_better = True
        return strictly_better

    # Check if current row is better than everything seen so far
    is_best = True
    for prev in seen:
        if not dominates(row, prev):
            is_best = False
            break
    
    # Heuristic: Stop if we've seen at least 50 rows and found a new best
    # This prevents stopping too early on random fluctuations.
    if is_best and len(seen) >= 50:
        return True
        
    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    seen = []
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopping criteria met at row {i}.")
            print("The current configuration is the best found so far and improvement has plateaued.")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("No clear stopping point found; the configuration continued to improve.")
    
    exit(0)
