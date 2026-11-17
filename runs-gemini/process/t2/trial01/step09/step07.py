import csv
from step01 import remember

def choose(header, rows, label):
    """
    We have 50 trials. We use a simple strategy:
    1. Sample 50 rows randomly (or spread out) to get a baseline.
    2. Label them to see their true goal values.
    3. Return the index of the best one found.
    """
    # We can label at most 50 rows.
    # We pick 50 indices spread across the dataset.
    n = len(rows)
    step = max(1, n // 50)
    indices_to_label = [i for i in range(0, n, step)][:50]
    
    best_idx = -1
    best_score = -1.0
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    is_max = [name.endswith('+') for name in header if name.endswith(('-', '+'))]
    
    for idx in indices_to_label:
        # Get true values
        goals = label(idx)
        
        # Calculate score
        row_score = 0
        for i, val in enumerate(goals):
            val = float(val)
            row_score += val if is_max[i] else (1.0 - val)
        
        avg_score = row_score / len(goal_indices)
        
        if avg_score > best_score:
            best_score = avg_score
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]
    
    # Store true values internally for the label function
    true_data = [
        [float(row[i]) for i, name in enumerate(header) if name.endswith(('-', '+'))]
        for row in rows
    ]
    
    def label(i):
        return true_data[i]
    
    best_row_idx = choose(header, rows, label)
    
    print(f"After trialing 50 setups, the best configuration found is at row index {best_row_idx}.")
    print(f"Goal values for this row: {label(best_row_idx)}")
