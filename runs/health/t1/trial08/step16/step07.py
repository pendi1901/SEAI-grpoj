import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup among 800 rows by sampling 50 rows, 
    labeling them, and picking the one with the highest aggregate score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(goals):
        # goals = [mre, acc, pred]
        # Normalize: (1 - MRE) + ACC + PRED. Higher is better.
        return (1.0 - goals[0]) + goals[1] + goals[2]

    # Select 50 random indices to sample
    indices = list(range(len(rows)))
    sample_indices = random.sample(indices, 50)
    
    best_idx = -1
    best_score = -float('inf')
    
    for i in sample_indices:
        # Get true goals from the harness
        goals = label(i)
        score = get_score(goals)
        
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                processed.append(val if header[i] == 'criterion' else float(val))
            rows.append(processed)
            
    # Store true goals to simulate the label function
    true_goals = [[r[0], r[1], r[2]] for r in rows]
    
    def label(i):
        return true_goals[i]
    
    # Mask rows for the choose function
    masked_rows = [r[:] for r in rows]
    for r in masked_rows:
        r[0], r[1], r[2] = "?", "?", "?"
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"Optimization complete. Best setup found at index {best_idx}.")
    print(f"Setup details: {rows[best_idx]}")
    print(f"Goals: MRE={rows[best_idx][0]:.4f}, ACC={rows[best_idx][1]:.4f}, PRED40={rows[best_idx][2]:.4f}")
