import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, labeling them, 
    and returning the index of the best one.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    # Identify min/max for normalization based on the first 50 labels
    # We sample 50 indices
    indices = list(range(len(rows)))
    # Use a fixed seed for reproducibility if needed, or random
    sample_indices = random.sample(indices, min(50, len(rows)))
    
    labeled_data = []
    for i in sample_indices:
        goals = label(i)
        labeled_data.append((goals, i))
    
    # Calculate scores for the sampled rows
    # Goals: MRE- (min), ACC+ (max), PRED40+ (max)
    # Normalize each goal column based on the 50 samples
    def get_score(goals):
        score = 0
        for j, g_idx in enumerate(goal_indices):
            col_name = header[g_idx]
            vals = [d[0][j] for d in labeled_data]
            mn, mx = min(vals), max(vals)
            norm = (goals[j] - mn) / (mx - mn) if mx > mn else 0
            if col_name.endswith('-'):
                score += (1 - norm)
            else:
                score += norm
        return score / len(goal_indices)

    best_idx = -1
    best_score = -1
    
    for goals, original_idx in labeled_data:
        s = get_score(goals)
        if s > best_score:
            best_score = s
            best_idx = original_idx
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Store true values to simulate the label function
    true_goals = []
    for r in rows:
        true_goals.append([r[i] for i, h in enumerate(header) if h.endswith(('-', '+'))])
        # Hide goals in the rows passed to choose
        for i, h in enumerate(header):
            if h.endswith(('-', '+')):
                r[i] = "?"

    def label(i):
        return true_goals[i]

    best_row_idx = choose(header, rows, label)
    print(f"The best setup found is at row index: {best_row_idx}")
    print(f"Configuration: {rows[best_row_idx]}")
    print(f"Performance goals: {true_goals[best_row_idx]}")
