import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, labeling them, 
    and picking the one with the best aggregate score.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # We have 800 rows, we can label 50.
    # We pick 50 indices to sample.
    indices = random.sample(range(len(rows)), 50)
    
    best_idx = -1
    best_score = -float('inf')
    
    # Pre-calculate global min/max for normalization based on the 50 samples
    # (Since we don't know the full dataset distribution, we use the samples)
    sampled_data = []
    for i in indices:
        goals = label(i)
        sampled_data.append(goals)
    
    # Transpose goals to get min/max
    goal_mins = [min(s[j] for s in sampled_data) for j in range(len(goal_indices))]
    goal_maxs = [max(s[j] for s in sampled_data) for j in range(len(goal_indices))]
    
    for idx, goals in zip(indices, sampled_data):
        # Calculate aggregate score
        score = 0
        for j, g_idx in enumerate(goal_indices):
            val = goals[j]
            rng = goal_maxs[j] - goal_mins[j] + 1e-9
            norm = (val - goal_mins[j]) / rng
            
            # MRE- (minimize): lower is better
            if header[g_idx].endswith('-'):
                score -= norm
            # ACC+/PRED40+ (maximize): higher is better
            else:
                score += norm
        
        if score > best_score:
            best_score = score
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Define the label function for the harness
        def label(i):
            # Return the goal values for the row
            return [rows[i][j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        
        best_idx = choose(header, rows, label)
        print(f"Analysis complete. The best setup found is at index {best_idx}.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
