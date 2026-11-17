import csv
from step01 import remember

def flow(header, row, seen):
    """
    Implements a Secretary Problem-style strategy.
    We observe a sample (first 20% of data) to establish a baseline 'best' 
    score, then accept the first row that exceeds that baseline.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    is_max = [name.endswith('+') for name in header if name.endswith(('-', '+'))]

    def get_score(r):
        s = 0
        for i, idx in enumerate(goal_indices):
            val = float(r[idx])
            s += val if is_max[i] else (1.0 - val)
        return s / len(goal_indices)

    # If we haven't seen enough to establish a baseline, keep looking
    # Using 20% of the expected 16000 rows (3200) as a sample period
    sample_size = 3200
    if len(seen) < sample_size:
        return False
    
    # Calculate the best score seen so far in the sample
    best_baseline = max(get_score(r) for r in seen)
    
    # If the current row is better than the best seen in the sample, accept it
    return get_score(row) > best_baseline

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
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
        print(f"Row details: {accepted}")
    else:
        print("Decision: No suitable proposal found.")
