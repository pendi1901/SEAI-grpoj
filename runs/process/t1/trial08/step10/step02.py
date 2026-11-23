import csv

def guess(header, train, test):
    """
    Estimates the first goal column for each test row using a 
    k-nearest neighbors approach based on input columns.
    """
    # Identify goal indices and input indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith(('-', '+')))]
    
    target_idx = goal_indices[0]
    
    def dist(row1, row2):
        # Euclidean distance on input columns
        d = 0
        for i in input_indices:
            v1, v2 = row1[i], row2[i]
            if isinstance(v1, float) and isinstance(v2, float):
                d += (v1 - v2) ** 2
            else:
                d += 0 if v1 == v2 else 1
        return d ** 0.5

    results = []
    for t_row in test:
        # Find nearest neighbor in training set
        best_d = float('inf')
        best_val = 0
        for train_row in train:
            d = dist(t_row, train_row)
            if d < best_d:
                best_d = d
                best_val = train_row[target_idx]
        results.append(best_val)
    return results

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Split data: use first 700 for training, next 100 for testing
        train_data = rows[:700]
        test_data = []
        for r in rows[700:]:
            new_row = list(r)
            # Mask goals in test data
            for idx in range(len(header)):
                if header[idx].endswith(('-', '+')):
                    new_row[idx] = "?"
            test_data.append(new_row)
            
        predictions = guess(header, train_data, test_data)
        
        # Print summary for the customer
        avg_cost = sum(predictions) / len(predictions)
        print(f"Analysis complete for {len(predictions)} setups.")
        print(f"Estimated average cost (first goal): {avg_cost:.4f}")
        print("These estimates are based on the nearest neighbor performance in historical data.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
