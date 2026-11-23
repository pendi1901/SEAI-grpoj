import csv
import random
from step01 import remember

def choose(header, rows, label):
    """
    Find the best setup by sampling 50 rows, labeling them, 
    and returning the index of the best one.
    """
    # Identify goal indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # We have 50 tries. We will sample 50 random rows.
    # To ensure we don't pick the same index twice, use sample.
    n_rows = len(rows)
    sample_size = min(50, n_rows)
    indices = random.sample(range(n_rows), sample_size)
    
    labeled_data = []
    for idx in indices:
        # Get true goals
        goals = label(idx)
        # Create a copy of the row with the true goals filled in
        row_with_goals = list(rows[idx])
        for i, g_idx in enumerate(goal_indices):
            row_with_goals[g_idx] = goals[i]
        labeled_data.append((row_with_goals, idx))
    
    # Use remember logic to rank the labeled rows
    # remember() expects a list of rows and returns indices of top 5%
    # We adapt by creating a temporary header/rows structure for remember
    best_idx_in_labeled = remember(header, [x[0] for x in labeled_data])[0]
    
    return labeled_data[best_idx_in_labeled][1]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Keep a copy of true goals to satisfy the label function
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    true_goals = [[r[i] for i in goal_indices] for r in rows]
    
    def label(i):
        return true_goals[i]

    # Mask rows for the choose function
    masked_rows = []
    for r in rows:
        masked = list(r)
        for i in goal_indices:
            masked[i] = "?"
        masked_rows.append(masked)

    best_idx = choose(header, masked_rows, label)
    
    print(f"Best setup found at index: {best_idx}")
    print("Setup details:")
    for h, v in zip(header, rows[best_idx]):
        print(f"  {h}: {v}")
