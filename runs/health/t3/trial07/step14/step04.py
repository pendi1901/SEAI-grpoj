import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to ship.
    We define 'good enough' as being better than all previously seen rows
    across all objectives (Pareto dominance).
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    # If it's the first row, we have no baseline, so keep looking
    if not seen:
        return False

    # Check if current row dominates any previous row
    # A row is 'good enough' if it is better than the best seen so far
    # or if it is a new Pareto optimal point.
    def dominates(row_a, row_b):
        better_or_equal = True
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

    # If the current row dominates all previously seen rows, it is a candidate
    # To avoid stopping too early, we require it to be significantly better
    # or simply better than the current 'best' aggregate.
    is_better_than_all = True
    for prev in seen:
        if not dominates(row, prev):
            is_better_than_all = False
            break
            
    return is_better_than_all

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Found a ship-worthy setup at index {i}.")
            print(f"Row data: {row}")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("No setup was found that dominated all previous ones.")
