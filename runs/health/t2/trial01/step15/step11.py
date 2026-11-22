import csv
import step01
import step02

def remember(header, rows):
    """
    Finds the setups most similar to the 'current' setup (the last row)
    and returns their indices, ranked by their multi-objective score.
    """
    # Identify the current setup (the last row)
    current_row = rows[-1]
    other_rows = rows[:-1]
    
    # Identify input columns (those not ending in - or +)
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('-') or name.endswith('+'))
    ]
    
    # Calculate Euclidean distance to the current setup
    # Pre-calculate ranges for normalization
    ranges = []
    for i in input_indices:
        col = [r[i] for r in other_rows if isinstance(r[i], (int, float))]
        if col:
            ranges.append((i, min(col), max(col)))
        else:
            ranges.append((i, 0, 1))

    def dist(row1, row2):
        d = 0
        for i, min_v, max_v in ranges:
            v1, v2 = row1[i], row2[i]
            if isinstance(v1, str):
                d += 0 if v1 == v2 else 1
            else:
                d += ((v1 - v2) / (max_v - min_v + 1e-9))**2
        return d**0.5

    # Find the 5 most similar setups
    distances = []
    for i, row in enumerate(other_rows):
        distances.append((dist(current_row, row), i))
    
    distances.sort(key=lambda x: x[0])
    similar_indices = [item[1] for item in distances[:5]]
    
    # Score these similar setups using step01 logic
    # We use the full dataset to normalize scores
    best_indices = step01.remember(header, [other_rows[i] for i in similar_indices])
    
    # Map back to original indices
    return [similar_indices[i] for i in best_indices]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed.append(float(val))
                    else:
                        processed.append(val)
                rows.append(processed)
        
        # The customer asks for setups like the one they use today (last row)
        best_indices = remember(header, rows)
        
        print("Setups most similar to your current configuration:")
        for idx in best_indices:
            row = rows[idx]
            print(f"Index {idx}: MRE-={row[0]:.4f}, ACC+={row[1]:.4f}, PRED40+={row[2]:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
