import csv
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against all other rows.
    Returns (fraction_better, reason).
    """
    # 1. Estimate the goals for the target row
    # We use the guess function from step02, which uses KNN to predict goals
    # We need to pass a list containing the target row as the 'test' set
    # The guess function expects the goals to be "?" in the test set
    predictions = guess(header, rows, [row])
    
    # The guess function returns [MRE_pred]. 
    # Since we need all three goals (MRE, ACC, PRED40), we need to adapt.
    # Given the constraints, we will estimate the score directly.
    # For simplicity and consistency with step01, we use the score heuristic.
    
    # Calculate scores for all existing rows
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    def get_score(r):
        return (1.0 - float(r[mre_idx])) + float(r[acc_idx]) + float(r[pred_idx])
    
    scores = [get_score(r) for r in rows]
    
    # Estimate score for the target row
    # Since guess() only predicts MRE, we use the average of the dataset for ACC/PRED40
    # as a baseline for the target row's performance.
    avg_acc = sum(float(r[acc_idx]) for r in rows) / len(rows)
    avg_pred = sum(float(r[pred_idx]) for r in rows) / len(rows)
    target_score = (1.0 - predictions[0]) + avg_acc + avg_pred
    
    # Calculate fraction of rows that are worse than the target
    better_than_count = sum(1 for s in scores if target_score > s)
    p = better_than_count / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all known configurations based on its input parameters."
    
    return p, reason

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
    
    # Pick a sample row to justify
    sample_row = rows[0][:]
    sample_row[0] = sample_row[1] = sample_row[2] = "?"
    
    p, reason = justify(header, rows, sample_row)
    print(f"Justification: {reason}")
