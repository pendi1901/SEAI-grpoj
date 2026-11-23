import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal column for each test row by finding the 
    nearest neighbor in the training set based on input columns.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Identify the first goal column index
    goal_idx = next(i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+'))

    def dist(row1, row2):
        # Euclidean distance on input columns
        d = 0
        for i in input_indices:
            d += (row1[i] - row2[i])**2
        return d**0.5

    results = []
    for t_row in test:
        # Find the row in train that is closest to t_row
        best_dist = float('inf')
        best_val = 0
        for train_row in train:
            d = dist(t_row, train_row)
            if d < best_dist:
                best_dist = d
                best_val = train_row[goal_idx]
        results.append(best_val)
    
    return results

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Split data: use first 700 for training, next 100 for testing
        train_data = rows[:700]
        test_data = [row[:] for row in rows[700:]]
        
        # Mask goals in test data
        goal_indices = [i for i, name in enumerate(header) 
                        if name.endswith('-') or name.endswith('+')]
        for row in test_data:
            for i in goal_indices:
                row[i] = "?"
        
        predictions = guess(header, train_data, test_data)
        
        # Print summary for the customer
        print("Estimating costs for the test set:")
        avg_cost = sum(predictions) / len(predictions)
        print(f"Average estimated {header[goal_indices[0]]}: {avg_cost:.4f}")
        print(f"Total rows analyzed: {len(predictions)}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
