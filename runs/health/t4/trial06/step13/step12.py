import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from step02 import guess as step02_guess

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) using a Random Forest Regressor.
    """
    return step02_guess(header, train, test)

def analyze_halving_impact(header, rows):
    """
    Analyzes the impact of halving 'N_estimators' on the first goal (MRE-).
    """
    n_idx = header.index('N_estimators')
    mre_idx = 0
    
    # Filter rows where halving is possible (N_estimators >= 2 * min_val)
    # We compare original rows vs rows with halved N_estimators
    valid_rows = [r for r in rows if r[n_idx] >= 20]
    
    # Create test set: original rows with halved N_estimators
    test_data = []
    for row in valid_rows:
        new_row = list(row)
        new_row[n_idx] = row[n_idx] / 2
        new_row[mre_idx] = "?"
        test_data.append(new_row)
    
    # Predict MRE- for halved setups
    predictions = guess(header, valid_rows, test_data)
    
    # Calculate average difference
    original_mre = [r[mre_idx] for r in valid_rows]
    diffs = [pred - orig for pred, orig in zip(predictions, original_mre)]
    
    return np.mean(diffs)

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

    avg_impact = analyze_halving_impact(header, rows)
    
    print("Impact Analysis of Halving N_estimators:")
    print(f"If you halve the size of the forecaster, the MRE- is estimated to change by {avg_impact:.4f} on average.")
    print("A positive value indicates performance degradation (higher MRE- is worse).")
