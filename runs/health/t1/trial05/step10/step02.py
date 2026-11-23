import csv

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    k-Nearest Neighbors approach based on Euclidean distance of 
    numeric input features.
    """
    mre_idx = 0
    # Identify input columns (those that are not goals)
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Normalize numeric inputs for distance calculation
    # We only care about numeric inputs for distance
    numeric_inputs = [i for i in input_indices if header[i] not in ['criterion']]
    
    # Precompute min/max for normalization
    mins = []
    maxs = []
    for i in numeric_inputs:
        vals = [r[i] for r in train]
        mins.append(min(vals))
        maxs.append(max(vals))
    
    def get_dist(row1, row2):
        d2 = 0
        for idx, i in enumerate(numeric_inputs):
            if maxs[idx] > mins[idx]:
                d2 += ((row1[i] - row2[i]) / (maxs[idx] - mins[idx]))**2
        # Add penalty for different symbolic values
        crit_idx = header.index('criterion')
        if row1[crit_idx] != row2[crit_idx]:
            d2 += 1.0
        return d2**0.5

    predictions = []
    k = 5
    for t_row in test:
        # Find k nearest neighbors in training set
        distances = []
        for train_row in train:
            distances.append((get_dist(t_row, train_row), train_row[mre_idx]))
        
        distances.sort(key=lambda x: x[0])
        # Average the MRE of the k nearest neighbors
        avg_mre = sum(d[1] for d in distances[:k]) / k
        predictions.append(avg_mre)
        
    return predictions

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['criterion']:
                        processed_row.append(val)
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
        
        # Split: use last 10 rows as a test set to demonstrate
        train_data = rows[:-10]
        test_data = [[val if header[i] not in ['MRE-', 'ACC+', 'PRED40+'] else "?" 
                      for i, val in enumerate(r)] for r in rows[-10:]]
        
        results = guess(header, train_data, test_data)
        
        print("Forecast estimation for the first goal (MRE-):")
        for i, val in enumerate(results):
            print(f"Test row {i+1}: Estimated MRE = {val:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
