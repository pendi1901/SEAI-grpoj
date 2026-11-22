import csv

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than 
    all previously seen rows. Uses a simple dominance check on goals.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def get_scores(r):
        scores = []
        for idx, op in goal_indices:
            val = float(r[idx])
            scores.append(val if op == '-' else -val)
        return scores

    current_scores = get_scores(row)

    # If this is the first row, accept it
    if not seen:
        return True

    # Compare against all previously seen rows
    # We accept if this row is better than or equal to all previous rows
    # (i.e., it is a non-dominated candidate in the sequence)
    for prev_row in seen:
        prev_scores = get_scores(prev_row)
        # Check if current row dominates or is equal to previous
        # If any previous row is strictly better, we reject
        for c, p in zip(current_scores, prev_scores):
            if c > p:
                return False
    
    return True

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        seen = []
        accepted_count = 0
        for row in rows:
            if flow(header, row, seen):
                accepted_count += 1
                seen.append(row)
        
        print(f"Analysis complete.")
        print(f"Processed {len(rows)} proposals.")
        print(f"Recommended to approve {accepted_count} proposals based on sequential dominance.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
