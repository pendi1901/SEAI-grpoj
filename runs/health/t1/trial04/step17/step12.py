import csv

def guess(header, train, test):
    """
    Estimates the first goal (MRE-) by comparing performance of 'full' 
    vs 'halved' N_estimators.
    """
    n_idx = header.index('N_estimators')
    goal_idx = 0
    
    # Calculate average MRE for full vs half
    # We define 'half' as N_estimators <= median
    vals = [r[n_idx] for r in train]
    median = sorted(vals)[len(vals) // 2]
    
    full_mres = [r[goal_idx] for r in train if r[n_idx] > median]
    half_mres = [r[goal_idx] for r in train if r[n_idx] <= median]
    
    avg_full = sum(full_mres) / len(full_mres) if full_mres else 0
    avg_half = sum(half_mres) / len(half_mres) if half_mres else 0
    
    # Return the average of the 'half' group for all test rows
    return [avg_half for _ in test]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
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
            rows.append(processed_row)
    
    # Split: train on 80%, test on 20%
    split = int(len(rows) * 0.8)
    train_data = rows[:split]
    test_data = rows[split:]
    
    # Mask test goals
    masked_test = []
    for r in test_data:
        new_row = list(r)
        for i, h in enumerate(header):
            if '-' in h or '+' in h:
                new_row[i] = "?"
        masked_test.append(new_row)
        
    # Calculate impact
    n_idx = header.index('N_estimators')
    vals = [r[n_idx] for r in train_data]
    median = sorted(vals)[len(vals) // 2]
    
    full = [r[0] for r in train_data if r[n_idx] > median]
    half = [r[0] for r in train_data if r[n_idx] <= median]
    
    avg_full = sum(full) / len(full)
    avg_half = sum(half) / len(half)
    diff = avg_half - avg_full
    
    print("Impact of halving N_estimators on MRE-:")
    print(f"Average MRE- (Full Size): {avg_full:.4f}")
    print(f"Average MRE- (Half Size): {avg_half:.4f}")
    print(f"Performance degradation: {diff:.4f} (MRE- increases, which is worse).")
