import csv
from step01 import remember

def justify(header, rows, row):
    """
    Returns a pair (p, reason) where p is the percentile rank of the row
    and reason is a human-readable explanation.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    is_max = [name.endswith('+') for name in header if name.endswith(('-', '+'))]

    def get_score(r):
        s = 0
        for i, idx in enumerate(goal_indices):
            val = float(r[idx])
            s += val if is_max[i] else (1.0 - val)
        return s / len(goal_indices)

    # Calculate scores for all existing rows
    all_scores = [get_score(r) for r in rows]
    
    # Estimate the score of the target row using the average of its nearest neighbors
    # (Using the logic from step02 to estimate the missing goal values)
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    best_dist = float('inf')
    best_neighbor = None
    for train_row in rows:
        dist = sum((float(row[i]) - float(train_row[i]))**2 for i in input_indices)
        if dist < best_dist:
            best_dist = dist
            best_neighbor = train_row
            
    # Calculate score for the target row using estimated goal values
    target_score = get_score(best_neighbor)
    
    # Calculate fraction of rows that are worse than this one
    better_than_count = sum(1 for s in all_scores if target_score > s)
    p = better_than_count / len(all_scores)
    
    reason = f"This setup outperforms {p:.1%} of all recorded configurations based on its projected performance metrics."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    # Pick a sample row and mask its goals to test the justify function
    sample_row = rows[0][:]
    for i in range(len(header)):
        if header[i].endswith(('-', '+')):
            sample_row[i] = "?"

    p, reason = justify(header, rows, sample_row)
    print(f"Percentile: {p:.4f}")
    print(f"Reason: {reason}")
