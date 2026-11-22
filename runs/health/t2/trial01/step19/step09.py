import csv
import step01

def spot(header, rows):
    """
    Identifies rows that are 'failed runs'. A failed run is defined here as 
    a row where the numeric input values are extreme outliers compared to 
    the rest of the population, suggesting a data entry error or a crash.
    """
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('-') or name.endswith('+')) and isinstance(rows[0][i], (int, float))
    ]
    
    # Calculate Z-scores for each numeric input column
    # A row is suspicious if it has a high cumulative Z-score across inputs
    n = len(rows)
    suspicion_scores = [0.0] * n
    
    for i in input_indices:
        col_vals = [r[i] for r in rows]
        mu = sum(col_vals) / n
        sigma = (sum((x - mu)**2 for x in col_vals) / n)**0.5
        
        if sigma > 0:
            for row_idx in range(n):
                z = abs(rows[row_idx][i] - mu) / sigma
                suspicion_scores[row_idx] += z
                
    # Pair scores with indices and sort descending
    indexed_scores = list(enumerate(suspicion_scores))
    indexed_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top 5% most suspicious indices
    limit = max(1, int(n * 0.05))
    return [item[0] for item in indexed_scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious = spot(header, rows)
        print("Analysis complete. Identified potentially failed/erroneous runs.")
        print(f"Most suspicious row indices: {suspicious[:10]}...")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
