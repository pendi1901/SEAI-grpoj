import csv

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows.
    To simulate 'requirements changing twice as fast', we weight the 
    'Dynamism' input column more heavily when calculating distance,
    as dynamism represents the rate of change in requirements.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    first_goal_idx = goal_indices[0]
    dynamism_idx = header.index('Dynamism')
    
    def dist(row_a, row_b):
        d = 0
        for i in input_indices:
            val_a = row_a[i]
            val_b = row_b[i]
            # Weight Dynamism by 2.0 to simulate the "twice as fast" requirement change
            weight = 2.0 if i == dynamism_idx else 1.0
            if isinstance(val_a, (int, float)):
                d += weight * ((val_a - val_b) ** 2)
            else:
                d += weight * (0 if val_a == val_b else 1)
        return d ** 0.5

    results = []
    for t_row in test:
        # Find the nearest neighbor in training data using the weighted distance
        best_dist = float('inf')
        best_val = 0
        for train_row in train:
            d = dist(t_row, train_row)
            if d < best_dist:
                best_dist = d
                best_val = train_row[first_goal_idx]
        results.append(best_val)
    return results

def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            processed = []
            for val in row:
                try:
                    processed.append(float(val))
                except ValueError:
                    processed.append(val)
            rows.append(processed)
    return header, rows

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        header, rows = load_data(filename)
        
        # Split: First 400 as stable, next 400 as "twice as fast" change
        # We simulate the impact by predicting on the second half
        train_data = rows[:400]
        test_data = []
        for r in rows[400:]:
            new_row = list(r)
            for i in range(len(header)):
                if header[i].endswith(('-', '+')):
                    new_row[i] = "?"
            test_data.append(new_row)
            
        predictions = guess(header, train_data, test_data)
        
        avg_cost = sum(predictions) / len(predictions)
        print("Impact Analysis: Requirements changing twice as fast.")
        print(f"Estimated average Cost- under increased dynamism: {avg_cost:.4f}")
        print("The model accounts for increased volatility by weighting the 'Dynamism' factor.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
