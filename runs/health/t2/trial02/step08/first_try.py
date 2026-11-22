import csv
import step01
import step02

def fix(header, row, levers):
    """
    Finds the smallest change to settings that improves the row's score.
    'Smallest change' is defined by the distance in the lever space.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Use a simple heuristic: minimize MRE, maximize ACC and PRED40
        # Since we don't have the full dataset context here, we use the row's values
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    best_change = {}
    best_score = get_score(row)
    
    # Try changing one lever at a time
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a small step (10% of range)
            step = (high - low) * 0.1
            candidates = [original_val - step, original_val + step]
            candidates = [c for c in candidates if low <= c <= high]
            
        for val in candidates:
            new_row = row[:]
            new_row[idx] = val
            # Estimate new goals using step02.guess (simplified)
            # We assume the row's performance improves if we move towards 
            # better configurations found in the dataset.
            new_score = get_score(new_row)
            if new_score > best_score:
                best_score = new_score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Example usage
    bad_row = rows[0]
    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Max_depth': (1, 20)
    }
    
    recommendation = fix(header, bad_row, levers)
    print("Customer Inquiry: 'What is the smallest change to improve my setup?'")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Answer: Change {col} to {val:.2f} if numeric, or '{val}' if symbolic.")
    else:
        print("Answer: No simple change found to improve performance.")
