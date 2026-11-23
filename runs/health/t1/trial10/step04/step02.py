import csv

def guess(header, train, test):
    """
    Estimates the first goal (MRE-) for each test row using a K-Nearest Neighbors 
    approach based on Euclidean distance of input features.
    """
    # Identify goal and input columns
    goal_idx = 0  # MRE-
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    def get_dist(row1, row2):
        d = 0
        for i in input_indices:
            val1, val2 = row1[i], row2[i]
            if isinstance(val1, str):
                d += 0 if val1 == val2 else 1
            else:
                # Normalize numeric distance
                d += (val1 - val2) ** 2
        return d ** 0.5

    predictions = []
    for t_row in test:
        # Find the 5 nearest neighbors in the training set
        distances = []
        for train_row in train:
            distances.append((get_dist(t_row, train_row), train_row[goal_idx]))
        
        distances.sort(key=lambda x: x[0])
        
        # Average the goal value of the 5 nearest neighbors
        k = 5
        neighbors = distances[:k]
        avg_mre = sum(n[1] for n in neighbors) / k
        predictions.append(avg_mre)
        
    return predictions

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
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
        
        # Split data: use 80% for training, 20% for testing
        split = int(len(rows) * 0.8)
        train_data = rows[:split]
        test_data = []
        for r in rows[split:]:
            # Mask the goals
            new_row = list(r)
            new_row[0] = new_row[1] = new_row[2] = "?"
            test_data.append(new_row)
            
        results = guess(header, train_data, test_data)
        
        print("Forecast estimation complete.")
        print(f"Estimated MRE for the first 5 test cases: {[round(x, 4) for x in results[:5]]}")
        print("These estimates are based on the average performance of the 5 most similar historical setups.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
