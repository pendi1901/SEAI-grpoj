import csv
import numpy as np
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the performance of 'row' and compares it against all 'rows'.
    Returns (fraction_better, reason_string).
    """
    # Identify indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # The guess function in step02 expects '?' in the goal columns.
    # However, it fails because it tries to cast '?' to float.
    # We create a wrapper to handle the '?' for the estimation.
    def estimate_goals(target_row):
        # We need to estimate MRE-, ACC+, and PRED40+.
        # Since step02.guess only estimates the first goal (MRE-),
        # we run it three times, once for each goal column.
        results = []
        for goal_idx in [mre_idx, acc_idx, pred_idx]:
            # Temporarily swap the goal column to be the first one for guess()
            # and mask the others.
            temp_header = [header[goal_idx]] + header[3:]
            temp_train = [[r[goal_idx]] + r[3:] for r in rows]
            temp_test = [['?'] + target_row[3:]]
            
            pred = guess(temp_header, temp_train, temp_test)
            results.append(pred[0])
        return results

    est_mre, est_acc, est_pred = estimate_goals(row)
    
    def score(mre, acc, pred):
        # MRE is minimize, ACC/PRED are maximize.
        return (1.0 - mre) + acc + pred
    
    target_score = score(est_mre, est_acc, est_pred)
    
    # Calculate scores for all existing rows
    all_scores = [score(r[mre_idx], r[acc_idx], r[pred_idx]) for r in rows]
    
    # Calculate fraction of rows that are worse than target_score
    better_than_count = sum(1 for s in all_scores if target_score > s)
    fraction = better_than_count / len(rows)
    
    reason = (f"This setup is estimated to outperform {fraction:.1%} of historical configurations "
              "based on a multi-objective analysis of MRE, ACC, and PRED metrics.")
    
    return float(fraction), reason

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
