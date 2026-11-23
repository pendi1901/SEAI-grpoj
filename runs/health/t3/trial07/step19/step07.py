import csv
import random

def choose(header, rows, label):
    """
    Selects the best setup by sampling 50 rows, labeling them, 
    and picking the one that dominates the others.
    """
    # Identify goal indices and directions
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    def get_score(row_goals):
        # Normalize goals to a simple score for comparison
        score = 0
        for i, (idx, direction) in enumerate(goals):
            val = row_goals[i]
            # Simple heuristic: normalize by direction
            score += val if direction == 1 else -val
        return score

    # Randomly sample 50 indices
    indices = random.sample(range(len(rows)), min(50, len(rows)))
    
    best_idx = -1
    best_score = float('-inf')
    
    for i in indices:
        # Label the row to get true goal values
        true_goals = label(i)
        
        # Calculate score
        score = get_score(true_goals)
        
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    full_rows = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            full_rows.append(processed_row)
            
            # Create masked row for the function
            masked_row = processed_row[:]
            for i, name in enumerate(header):
                if name.endswith(('-', '+')):
                    masked_row[i] = "?"
            rows.append(masked_row)

    # Define label function for the harness
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def label(i):
        return [full_rows[i][idx] for idx in goal_indices]

    best_idx = choose(header, rows, label)
    
    print(f"After evaluating 50 setups, the best configuration found is at index {best_idx}.")
    print(f"Configuration details: {full_rows[best_idx]}")
