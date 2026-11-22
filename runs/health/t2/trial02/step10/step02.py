import csv
import step01

def guess(header, train, test):
    """
    Estimates the MRE- (first goal column) for test rows using a 
    k-Nearest Neighbors approach based on input columns.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('-') or name.endswith('+'))
    ]
    
    # Identify the target column (first goal column)
    target_idx = 0 
    
    predictions = []
    
    for t_row in test:
        distances = []
        for train_row in train:
            dist = 0
            for i in input_indices:
                # Handle symbolic vs numeric inputs
                if isinstance(t_row[i], str):
                    if t_row[i] != train_row[i]:
                        dist += 1
                else:
                    # Simple Euclidean distance for numeric inputs
                    dist += (t_row[i] - train_row[i])**2
            distances.append((dist, train_row[target_idx]))
        
        # Sort by distance and take the average of the 5 nearest neighbors
        distances.sort(key=lambda x: x[0])
        k = 5
        neighbors = distances[:k]
        avg_mre = sum(n[1] for n in neighbors) / k
        predictions.append(avg_mre)
        
    return predictions

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

    # Create a dummy test set from the last 5 rows to demonstrate the guess function
    test_data = [r[:] for r in rows[-5:]]
    for row in test_data:
        row[0] = "?" # MRE-
        row[1] = "?" # ACC+
        row[2] = "?" # PRED40+

    estimates = guess(header, rows[:-5], test_data)
    
    print("Customer Inquiry: 'How far off will my forecasts be?'")
    print("Estimation for the first 5 test setups (MRE-):")
    for i, val in enumerate(estimates):
        print(f"Setup {i+1}: Estimated MRE = {val:.4f}")
