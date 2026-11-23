import csv
import random

def get_score(header, row):
    """
    Calculates aggregate score: (1 - MRE) + ACC + PRED40.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    return (1.0 - float(row[mre_idx])) + float(row[acc_idx]) + float(row[pred_idx])

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing and small.
    We define 'small' as having a low N_estimators value.
    We sample 50 rows, calculate a weighted score (performance - penalty for size),
    and return the index of the best one.
    """
    n_idx = header.index('N_estimators')
    
    # Sample 50 indices
    indices = random.sample(range(len(rows)), min(50, len(rows)))
    
    best_idx = -1
    best_val = -float('inf')
    
    for i in indices:
        goals = label(i)
        # Reconstruct row with goals
        row = list(rows[i])
        row[header.index('MRE-')] = goals[0]
        row[header.index('ACC+')] = goals[1]
        row[header.index('PRED40+')] = goals[2]
        
        perf = get_score(header, row)
        # Penalty for size: normalize N_estimators (range ~10-200)
        # We want to minimize size, so we subtract a fraction of it from performance
        size = float(row[n_idx])
        size_penalty = (size / 200.0) * 0.2
        
        score = perf - size_penalty
        
        if score > best_val:
            best_val = score
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
            processed_row = []
            for i, val in enumerate(row):
                # criterion is at index 4
                if i == 4:
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    goal_indices = [header.index('MRE-'), header.index('ACC+'), header.index('PRED40+')]
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
        
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"Recommended setup found at index {best_idx}.")
    print("This configuration balances high predictive accuracy with a small footprint,")
    print("making it ideal for nightly execution.")
