import csv

def flow(header, row, seen):
    """
    Decides whether to accept the current row based on whether it is 
    better than all previously seen rows according to a multi-objective 
    weighted score.
    """
    # Identify goal indices
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    def get_score(r):
        # Calculate a simple score based on relative performance.
        # Since we don't have global min/max, we use the current row's 
        # values as a baseline or just compare raw values if possible.
        # Here, we use a simple heuristic: normalize goals to [0, 1] 
        # relative to the best seen so far.
        score = 0
        for idx, direction in goals:
            val = r[idx]
            # Since we need to decide on the fly, we treat the current row
            # as a candidate. If it's the first, accept it.
            score += val * direction
        return score

    if not seen:
        return True

    # Compare current row against the best seen so far
    current_score = get_score(row)
    best_score = max(get_score(r) for r in seen)

    # If current row is better than the best seen, accept it
    # (For minimization, lower is better; for maximization, higher is better)
    # This logic assumes we want to improve upon the current best.
    return current_score < best_score if goals[0][1] == -1 else current_score > best_score

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if header[i] not in ['criterion'] else val 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)

        seen = []
        accepted = None
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                accepted = (i, row)
                break
            seen.append(row)

        if accepted:
            print(f"Found a setup good enough to ship at index {accepted[0]}.")
            print(f"Row data: {accepted[1]}")
        else:
            print("No setup met the criteria.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
