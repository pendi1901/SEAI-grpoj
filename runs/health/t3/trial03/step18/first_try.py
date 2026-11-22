import csv

def fix(header, row, levers):
    """
    Recommends a single-lever change to improve a 'bad' row.
    It identifies the best-performing rows in the dataset and suggests
    the most frequent value for each lever found in those top-tier rows.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(r):
        score = 0
        for i in goal_indices:
            direction = -1 if header[i].endswith('-') else 1
            score += r[i] * direction
        return score

    # Load global rows (assumed to be available in the module scope)
    # If not available, we rely on the logic provided by the harness context
    global rows_global
    
    # Calculate scores to find the top 10% of configurations
    scored = sorted([(get_score(r), i) for i, r in enumerate(rows_global)], reverse=True)
    top_indices = [idx for _, idx in scored[:max(1, len(rows_global) // 10)]]
    
    # For each allowed lever, find the most popular value among top performers
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        counts = {}
        for idx in top_indices:
            val = rows_global[idx][col_idx]
            counts[val] = counts.get(val, 0) + 1
        
        if not counts:
            continue
            
        best_val = max(counts, key=counts.get)
        
        # Validate and return the first valid improvement
        if isinstance(allowed, list):
            if best_val in allowed and best_val != row[col_idx]:
                return {col_name: best_val}
        else:
            low, high = allowed
            if low <= best_val <= high and abs(best_val - row[col_idx]) > 1e-6:
                return {col_name: best_val}
                
    return {}

rows_global = []

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows_global.append(processed_row)

    levers = {
        'N_estimators': (10.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    # Identify the worst row to demonstrate the fix
    scores = [(sum(r[i] * (-1 if header[i].endswith('-') else 1) for i in range(len(header)) if header[i].endswith(('-', '+'))), i) for i, r in enumerate(rows_global)]
    bad_idx = min(scores)[1]
    bad_row = rows_global[bad_idx]

    recommendation = fix(header, bad_row, levers)

    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve your setup, change '{col}' to {val}.")
    else:
        print("No single-lever change found to improve performance.")
