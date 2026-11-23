import csv
import random
from step01 import remember

def get_score(header, row):
    """
    Calculates a composite score.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    Score = (1 - MRE) + ACC + PRED40.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    return (1.0 - float(row[mre_idx])) + float(row[acc_idx]) + float(row[pred_idx])

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing and 'small' (low N_estimators).
    We sample 50 rows, calculate a score that balances performance and 
    computational efficiency (penalizing high N_estimators).
    """
    n_est_idx = header.index('N_estimators')
    
    # Sample 50 indices
    indices_to_sample = random.sample(range(len(rows)), 50)
    
    best_score = -float('inf')
    best_idx = -1
    
    for i in indices_to_sample:
        goals = label(i)
        # Reconstruct row with goals
        row = [goals[0], goals[1], goals[2]] + rows[i][3:]
        
        # Performance score
        perf = get_score(header, row)
        
        # Efficiency penalty: normalize N_estimators (range 50-200)
        # We want small N_estimators, so we subtract a normalized cost
        n_est = float(row[n_est_idx])
        cost = (n_est - 50) / 150.0
        
        # Combined score: performance - cost
        combined = perf - (cost * 0.2)
        
        if combined > best_score:
            best_score = combined
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    full_data = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            full_data.append(processed_row)
            
    masked_rows = []
    for r in full_data:
        masked = r[:]
        masked[0] = masked[1] = masked[2] = "?"
        masked_rows.append(masked)
        
    def label(i):
        return [full_data[i][0], full_data[i][1], full_data[i][2]]
    
    best_index = choose(header, masked_rows, label)
    
    print(f"Analysis complete. Found a high-performing, efficient setup at index {best_index}.")
    print(f"Setup details: {full_data[best_index]}")
