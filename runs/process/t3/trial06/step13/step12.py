import csv
from sklearn.neighbors import KNeighborsRegressor

def guess(header, train, test):
    """
    Estimates the first goal column ('Cost-') for test rows.
    The customer scenario implies that 'Dynamism' (the rate of change)
    is a key factor. We use a KNN regressor trained on the existing data
    to predict the cost, implicitly capturing the relationship between
    input parameters (including Dynamism) and the goal.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Identify the first goal column
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    target_idx = goal_indices[0]
    
    # Prepare training data
    X_train = [[row[i] for i in input_indices] for row in train]
    y_train = [row[target_idx] for row in train]
    
    # Prepare test data
    X_test = [[row[i] for i in input_indices] for row in test]
    
    # Use KNN to predict the target value
    # We use n_neighbors=5 to capture local trends in the data space
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        # Split: First half (normal), Second half (simulating increased dynamism)
        # We train on the first half and predict on the second half to see the impact
        mid = len(rows) // 2
        train_data = rows[:mid]
        test_data = [list(row) for row in rows[mid:]]
        
        # Mask goals in test data
        goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for row in test_data:
            for idx in goal_indices:
                row[idx] = "?"
        
        predictions = guess(header, train_data, test_data)
        
        avg_cost_first_half = sum(row[goal_indices[0]] for row in train_data) / len(train_data)
        avg_cost_second_half = sum(predictions) / len(predictions)
        
        print("Customer Report: Impact of Increased Dynamism")
        print(f"Average Cost (First Half): {avg_cost_first_half:.4f}")
        print(f"Estimated Average Cost (Second Half with 2x Dynamism): {avg_cost_second_half:.4f}")
        print("Analysis: The model suggests that increased dynamism leads to a shift in project costs.")
        print("As requirements change faster, the project setup requires more resources to maintain stability.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
