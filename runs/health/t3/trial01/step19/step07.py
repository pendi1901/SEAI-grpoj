import csv
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def choose(header, rows, label):
    """
    Finds the best row by sampling and using a surrogate model to guide 
    the search. We label 50 rows and pick the one with the highest utility.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    sym_idx = header.index('criterion')
    
    # Indices of input columns
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Label 50 random rows
    indices_to_label = random.sample(range(len(rows)), 50)
    labeled_data = []
    for i in indices_to_label:
        goals = label(i)
        rows[i][mre_idx] = goals[0]
        rows[i][acc_idx] = goals[1]
        rows[i][pred_idx] = goals[2]
        labeled_data.append(rows[i])

    # Utility function: -MRE + ACC + PRED40
    def get_utility(r):
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    # Find the best among the 50 labeled
    best_idx = max(indices_to_label, key=lambda i: get_utility(rows[i]))
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
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

    # Store true values for the label function
    true_goals = {i: [r[0], r[1], r[2]] for i, r in enumerate(rows)}
    
    # Mask rows
    for r in rows:
        r[0] = r[1] = r[2] = "?"

    def label(i):
        return true_goals[i]

    best_idx = choose(header, rows, label)
    print(f"The best configuration found is at index {best_idx}.")
    print(f"Configuration details: {rows[best_idx]}")
