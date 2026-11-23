import csv

def flow(header, row, seen):
    """
    Decides whether to accept a row based on the 'Secretary Problem' logic.
    We observe the first 20% of rows to establish a baseline (the best seen so far),
    then accept the first row that is better than that baseline.
    """
    # Identify goal indices
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_row(r):
        total = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            if op == '-':
                total += val
            else:
                total += (1.0 - val)
        return total

    # If this is the first row, we must let it go to start building a baseline
    if not seen:
        return False

    # Calculate the best score seen so far
    best_seen_score = min(score_row(r) for r in seen)
    
    # Strategy: 
    # 1. Observe for the first 20% of the total expected population (approx 160 rows)
    # 2. After that, accept if the current row is better than the best seen so far.
    # 3. If we reach the last few rows, accept the best available.
    
    current_score = score_row(row)
    
    # If we are in the exploration phase (first 20%), keep looking
    if len(seen) < 160:
        return False
    
    # If we are at the very end, accept if it's better than the best seen
    # Otherwise, accept if it beats the baseline
    if current_score < best_seen_score:
        return True
        
    return False

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
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
            
        print("Customer Inquiry: Decision on incoming program proposals")
        print("-" * 60)
        if accepted:
            print("Decision: Approved the following proposal:")
            for h, v in zip(header, accepted):
                print(f"  {h}: {v}")
        else:
            print("Decision: No proposal met the criteria for approval.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
