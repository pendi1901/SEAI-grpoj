import csv
import step01

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    Uses a simple k-Nearest Neighbors approach based on numeric input columns.
    """
    # Identify the first goal column
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    # Identify numeric input columns (excluding goals)
    input_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and i != goal_idx
    ]
    
    predictions = []
    for t_row in test:
        # Simple distance: Euclidean distance on numeric inputs
        distances = []
        for r_row in train:
            dist = 0
            for i in input_indices:
                dist += (t_row[i] - r_row[i]) ** 2
            distances.append((dist**0.5, r_row[goal_idx]))
        
        # Sort by distance and take the average of the 5 nearest neighbors
        distances.sort(key=lambda x: x[0])
        k = 5
        neighbors = distances[:k]
        avg_val = sum(n[1] for n in neighbors) / k
        predictions.append(float(avg_val))
        
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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    results = guess(header, train_data, masked_test)
    
    print("Estimation of 'YearsAtCompany+' for new hires:")
    print(f"{'Row':<10} | {'Estimated Years'}")
    print("-" * 30)
    for i, val in enumerate(results[:10]): # Print first 10
        print(f"{i:<10} | {val:.2f}")
