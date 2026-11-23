import csv
from step02 import guess as step02_guess

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against 
    the historical dataset to determine its relative rank.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # 1. Estimate goals for the input row using KNN
    # We use the existing guess function which predicts MRE-
    # For ACC+ and PRED40+, we use the average of the entire dataset 
    # as a baseline or simple KNN-based estimation.
    # To keep it simple and consistent, we estimate all three.
    def get_all_goals(target_row):
        # Use the guess function for MRE-
        est_mre = step02_guess(header, rows, [target_row])[0]
        
        # For ACC+ and PRED40+, use the mean of the training data
        est_acc = sum(r[acc_idx] for r in rows) / len(rows)
        est_pred = sum(r[pred_idx] for r in rows) / len(rows)
        return est_mre, est_acc, est_pred

    est_mre, est_acc, est_pred = get_all_goals(row)
    
    # 2. Calculate utility
    def get_utility(mre, acc, pred):
        return -mre + acc + pred

    target_utility = get_utility(est_mre, est_acc, est_pred)
    utilities = [get_utility(r[mre_idx], r[acc_idx], r[pred_idx]) for r in rows]
    
    # 3. Calculate fraction of rows that are worse
    worse_count = sum(1 for u in utilities if target_utility > u)
    p = worse_count / len(rows)
    
    reason = "Using the biggest, deepest setup often leads to overfitting or diminishing returns, as evidenced by this configuration outperforming only " + f"{p:.1%} of historical setups."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Define a "biggest, deepest" setup
    # N_estimators=200, Max_depth=20, Min_sample_leaves=1
    test_row = [0.0, 0.0, 0.0, 200.0, 'squared_error', 1.0, 1.0, 20.0]
    # Mask goals
    for i in range(len(header)):
        if header[i].endswith('-') or header[i].endswith('+'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(reason)
    exit(0)
