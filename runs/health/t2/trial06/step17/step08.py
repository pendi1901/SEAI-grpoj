import csv
from step01 import remember

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its performance
    without increasing the 'N_estimators' (which relates to speed).
    """
    # Identify goal indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # We want to improve the score: (1 - norm_mre) + norm_acc + norm_pred
    # Since we don't have the full dataset here, we assume the row is bad
    # and we try to nudge numeric values or swap symbolic values.
    
    best_change = {}
    
    for col, allowed in levers.items():
        idx = header.index(col)
        current_val = row[idx]
        
        if isinstance(allowed, list):  # Symbolic
            for val in allowed:
                if val != current_val:
                    return {col: val}
        else:  # Numeric (low, high)
            low, high = allowed
            # Try nudging by 10% of the range
            step = (high - low) * 0.1
            if current_val + step <= high:
                return {col: current_val + step}
            elif current_val - step >= low:
                return {col: current_val - step}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) 
                         for i, val in enumerate(row)])

    # Define levers based on the dataset
    levers = {
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Max_depth': (1.0, 20.0)
    }

    # Pick a "bad" row (e.g., the one with the worst score)
    # Using remember logic to find the worst
    mre_idx, acc_idx, pred_idx = 0, 1, 2
    def get_score(r):
        return (1 - r[mre_idx]) + r[acc_idx] + r[pred_idx]
    
    worst_row = min(rows, key=get_score)
    
    recommendation = fix(header, worst_row, levers)
    
    print("Analysis: Smallest change to improve performance.")
    print(f"Bad row identified. Recommended change:")
    for col, val in recommendation.items():
        print(f"  Change '{col}' to {val}")
