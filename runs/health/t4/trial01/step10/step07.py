import csv
import random
from step01 import remember

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 configurations, labeling them,
    and returning the index of the one with the highest aggregate score.
    """
    # Identify indices for goals
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    # We have 800 rows. We can sample 50.
    # To be robust, we pick 50 random indices.
    indices = random.sample(range(len(rows)), 50)
    
    best_idx = -1
    best_score = -float('inf')
    
    for i in indices:
        # Get true values from the oracle
        goals = label(i)
        mre, acc, pred = goals[idx_mre], goals[idx_acc], goals[idx_pred]
        
        # Calculate aggregate score (Minimize MRE-, Maximize ACC+, Maximize PRED40+)
        # Normalize: (1 - MRE) + ACC + PRED
        score = (1.0 - mre) + acc + pred
        
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed.append(float(val))
                else:
                    processed.append(val)
            rows.append(processed)

    # Define the label function for the harness
    def label(i):
        return [rows[i][0], rows[i][1], rows[i][2]]

    # Mask the goals for the choose function
    masked_rows = []
    for row in rows:
        masked_rows.append(["?" if i < 3 else val for i, val in enumerate(row)])

    best_index = choose(header, masked_rows, label)
    
    print(f"Search complete. The best configuration found among the 50 sampled is at index {best_index}.")
    print(f"Configuration details: {rows[best_index]}")
