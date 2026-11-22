import csv
import numpy as np
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the performance of 'row' and compares it against all 'rows'.
    Returns (fraction_better, reason_string).
    """
    # 1. Estimate the goals for the target row
    # We need to treat the target row as a test set of size 1
    # Use step02's guess function logic
    predictions = guess(header, rows, [row])
    estimated_mre = predictions[0]
    
    # Since we only estimate MRE-, we assume ACC+ and PRED40+ are 
    # approximated by the mean of the training set for the comparison
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    mre_idx = header.index('MRE-')
    
    avg_acc = np.mean([r[acc_idx] for r in rows])
    avg_pred = np.mean([r[pred_idx] for r in rows])
    
    def score(mre, acc, pred):
        return (1.0 - mre) + acc + pred
    
    target_score = score(estimated_mre, avg_acc, avg_pred)
    
    # 2. Calculate scores for all existing rows
    all_scores = [score(r[mre_idx], r[acc_idx], r[pred_idx]) for r in rows]
    
    # 3. Calculate fraction of rows that are worse than target_score
    better_than_count = sum(1 for s in all_scores if target_score > s)
    fraction = better_than_count / len(rows)
    
    reason = (f"This setup is estimated to outperform {fraction:.1%} of historical configurations "
              "based on a multi-objective analysis of MRE, ACC, and PRED metrics.")
    
    return fraction, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i].isupper() or header[i] in ['N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Pick a sample row to justify (e.g., the last one)
    target_row = ['?'] * 3 + rows[-1][3:]
    
    p, reason = justify(header, rows, target_row)
    print(f"Performance Rank: {p:.4f}")
    print(f"Justification: {reason}")
