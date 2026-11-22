import csv
from step02 import guess

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
    # We need to pass it in a way that it treats the single row as a test set.
    train_data = [r for r in rows if r[mre_idx] != "?"]
    
    # guess() expects test data to have "?" in goal columns
    test_row = [row[:]]
    
    predictions = guess(header, train_data, test_row)
    est_mre = predictions[0]
    
    # 2. Calculate scores for all rows to compare
    # We must use the actual values for the population
    mre_vals = [r[mre_idx] for r in rows if r[mre_idx] != "?"]
    acc_vals = [r[acc_idx] for r in rows if r[acc_idx] != "?"]
    pred_vals = [r[pred_idx] for r in rows if r[pred_idx] != "?"]
    
    min_mre, max_mre = min(mre_vals), max(mre_vals)
    min_acc, max_acc = min(acc_vals), max(acc_vals)
    min_pred, max_pred = min(pred_vals), max(pred_vals)
    
    def get_score(mre, acc, pred):
        n_mre = (max_mre - mre) / (max_mre - min_mre) if max_mre > min_mre else 0
        n_acc = (acc - min_acc) / (max_acc - min_acc) if max_acc > min_acc else 0
        n_pred = (pred - min_pred) / (max_pred - min_pred) if max_pred > min_pred else 0
        return n_mre + n_acc + n_pred
    
    # The target row's estimated score
    target_score = get_score(est_mre, row[acc_idx], row[pred_idx])
    
    # 3. Calculate percentile
    all_scores = [get_score(r[mre_idx], r[acc_idx], r[pred_idx]) for r in rows if r[mre_idx] != "?"]
    better_than_count = sum(1 for s in all_scores if target_score > s)
    p = better_than_count / len(all_scores)
    
    reason = f"This configuration outperforms {p:.1%} of all tested setups based on its predicted multi-objective performance score."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])
    
    # Pick a sample row to justify
    sample_row = rows[-1][:]
    # Mask goals
    for i in range(3):
        rows[-1][i] = "?"
        
    p, reason = justify(header, rows, rows[-1])
    print(f"Score: {p:.4f}")
    print(reason)
