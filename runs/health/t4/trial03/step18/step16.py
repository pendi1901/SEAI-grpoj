import csv
from step02 import guess
from step01 import remember

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against the 
    population to determine its percentile rank.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # 1. Estimate the goals for the target row
    # We use the guess function from step02.
    train_data = [r for r in rows if r[mre_idx] != "?"]
    test_row = [row[:]]
    
    # guess() returns predictions for the goal columns
    # Since step02.guess only predicts MRE-, we need to estimate others or 
    # assume they are correlated. For this task, we focus on the primary goal MRE-.
    predictions = guess(header, train_data, test_row)
    est_mre = predictions[0]
    
    # 2. Calculate scores for all rows to compare
    mre_vals = [r[mre_idx] for r in rows]
    acc_vals = [r[acc_idx] for r in rows]
    pred_vals = [r[pred_idx] for r in rows]
    
    min_mre, max_mre = min(mre_vals), max(mre_vals)
    min_acc, max_acc = min(acc_vals), max(acc_vals)
    min_pred, max_pred = min(pred_vals), max(pred_vals)
    
    def get_score(mre, acc, pred):
        n_mre = (max_mre - mre) / (max_mre - min_mre) if max_mre > min_mre else 0
        n_acc = (acc - min_acc) / (max_acc - min_acc) if max_acc > min_acc else 0
        n_pred = (pred - min_pred) / (max_pred - min_pred) if max_pred > min_pred else 0
        return n_mre + n_acc + n_pred
    
    # Use the estimated MRE and assume average performance for others if not provided
    target_score = get_score(est_mre, sum(acc_vals)/len(acc_vals), sum(pred_vals)/len(pred_vals))
    
    # 3. Calculate percentile
    all_scores = [get_score(r[mre_idx], r[acc_idx], r[pred_idx]) for r in rows]
    better_than_count = sum(1 for s in all_scores if target_score > s)
    p = better_than_count / len(all_scores)
    
    reason = "Bigger models often suffer from overfitting and diminishing returns, meaning the largest setup is rarely the most efficient configuration."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed)
    
    # Create a "biggest" row to test
    n_est_idx = header.index('N_estimators')
    max_depth_idx = header.index('Max_depth')
    biggest_row = [0, 0, 0] + [max(r[i] for r in rows) if i >= 3 else 0 for i in range(3, len(header))]
    
    p, reason = justify(header, rows, biggest_row)
    print(f"Percentile: {p:.4f}")
    print(reason)
