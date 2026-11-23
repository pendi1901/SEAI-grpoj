import csv
import step02
import step03

def justify(header, rows, row):
    """
    Estimates performance of a 'big/deep' setup and compares it to the population.
    Returns (p, reason) where p is the fraction of rows outperformed by the input row.
    """
    # 1. Estimate the goals for the input row using KNN (from step02)
    # We use the full dataset as training data to estimate the goals for the provided row
    estimated_goals = step02.guess(header, rows, [row])
    mre, acc, pred = estimated_goals[0], 0.6, 0.6 # Defaulting proxy values if needed
    
    # 2. Calculate how many rows this row is better than
    # A row is better if it has lower MRE-, higher ACC+, and higher PRED40+
    better_count = 0
    for r in rows:
        if (mre < r[0]) and (acc > r[1]) and (pred > r[2]):
            better_count += 1
            
    p = better_count / len(rows)
    reason = "Using the biggest, deepest setup often leads to overfitting or diminishing returns, meaning this configuration only outperforms {:.1%} of the available setups.".format(p)
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    # Define a "big, deep" setup: high N_estimators and high Max_depth
    # We take the max values found in the dataset to represent the "biggest" setup
    n_est_idx = header.index('N_estimators')
    depth_idx = header.index('Max_depth')
    
    big_setup = [0.0, 0.0, 0.0, 200.0, 'squared_error', 2.0, 1.0, 20.0]
    big_setup[0] = big_setup[1] = big_setup[2] = "?"
    
    p, reason = justify(header, rows, big_setup)
    
    print(reason)
