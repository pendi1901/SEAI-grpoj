import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to approve a row based on whether it is better than
    the best seen so far. We use the logic from step01 to define 'better'.
    """
    if not seen:
        return True
    
    # Identify goal indices and directions
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_row(r):
        total = 0
        for idx, op in goal_indices:
            val = float(r[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # Compare current row against the best seen so far
    current_score = score_row(row)
    best_seen_score = min(score_row(r) for r in seen)
    
    # If the current row is better (lower score) than the best seen, approve it.
    # We also approve if it's the first one, but the loop handles that.
    return current_score < best_seen_score

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
            
            approved = []
            seen = []
            for row in rows:
                if flow(header, row, seen):
                    approved.append(row)
                seen.append(row)
            
            print(f"Customer Inquiry: Sequential approval process.")
            print(f"Total rows processed: {len(rows)}")
            print(f"Total approved: {len(approved)}")
            print("Decision strategy: Approve if the current row is better than all previous.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
