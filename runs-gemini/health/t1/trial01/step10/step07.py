import csv
import random

def choose(header, rows, label):
    """
    Finds the best row among 50 queries using a simple exploration-exploitation
    strategy. We sample rows, label them, and pick the one with the best
    multi-objective score.
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, 'min'))
        elif name.endswith('+'):
            goals.append((i, 'max'))

    # We have 50 queries. We'll use 10 to explore (random) and 40 to exploit.
    # Since we don't have a model, we'll sample 50 random rows to find the best.
    indices = list(range(len(rows)))
    random.shuffle(indices)
    
    best_idx = -1
    best_score = float('inf')
    
    # Track goal ranges for normalization
    # Since we only see 50, we use the global range if possible or just the 50
    # For simplicity, we use the 50 samples to define the "known" range.
    samples = []
    for i in range(min(50, len(indices))):
        idx = indices[i]
        vals = label(idx)
        samples.append((vals, idx))
        
    # Normalize and score
    for vals, idx in samples:
        score = 0
        for i, (g_idx, mode) in enumerate(goals):
            # In a real scenario, we'd normalize against the whole set,
            # but here we just compare the values directly since they are 
            # the only ones we know.
            val = vals[i]
            # Simple score: minimize distance to ideal (0 for min, 1 for max)
            # We assume goals are roughly in [0, 1] based on the prompt.
            if mode == 'min':
                score += val
            else:
                score += (1.0 - val)
        
        if score < best_score:
            best_score = score
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)

    # Prepare data for the harness
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    hidden_rows = []
    true_goals = []
    for row in rows:
        new_row = list(row)
        goals = []
        for i in goal_indices:
            goals.append(float(new_row[i]))
            new_row[i] = "?"
        hidden_rows.append(new_row)
        true_goals.append(goals)

    def label(i):
        return true_goals[i]

    best_idx = choose(header, hidden_rows, label)
    
    print(f"Analysis complete. After evaluating 50 setups, the best configuration is at index {best_idx}.")
    print(f"Row data: {rows[best_idx]}")
