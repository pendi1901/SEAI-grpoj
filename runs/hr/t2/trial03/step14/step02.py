import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    Uses a simple K-Nearest Neighbors approach based on numeric input columns.
    """
    # Identify the first goal column
    goal_col = [h for h in header if h.endswith('+') or h.endswith('-')][0]
    goal_idx = header.index(goal_col)
    
    # Identify numeric input columns (excluding goals)
    input_indices = [
        i for i, h in enumerate(header) 
        if h[0].isupper() and not (h.endswith('+') or h.endswith('-'))
    ]
    
    predictions = []
    
    for t_row in test:
        # Calculate Euclidean distance to all training rows
        distances = []
        for r_row in train:
            dist = 0
            for i in input_indices:
                # Normalize distance calculation
                dist += (t_row[i] - r_row[i]) ** 2
            distances.append((dist**0.5, r_row[goal_idx]))
        
        # Sort by distance and take average of top 5 neighbors
        distances.sort(key=lambda x: x[0])
        top_k = distances[:5]
        avg_val = sum(d[1] for d in top_k) / len(top_k)
        predictions.append(avg_val)
        
    return predictions

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Mask the goal column in test data
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+')][0]
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = 0.0 # Placeholder
        masked_test.append(new_row)
        
    results = guess(header, train_data, masked_test)
    
    print("Estimation for 'YearsAtCompany+' (First 5 test rows):")
    for i in range(5):
        print(f"Row {i}: Estimated {results[i]:.2f} years")
