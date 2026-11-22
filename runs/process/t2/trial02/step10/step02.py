import csv
from step01 import remember

def guess(header, train, test):
    """
    Estimates the first goal column for test rows by finding the 
    average of the first goal column from the top 5% of training rows.
    """
    # Find the index of the first goal column
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_idx = i
            break
    
    # Get indices of top-performing rows from step01
    best_indices = remember(header, train)
    
    # Calculate the average of the first goal column for these best rows
    total_val = sum(float(train[i][goal_idx]) for i in best_indices)
    avg_val = total_val / len(best_indices)
    
    # Return the estimate for each test row
    return [avg_val for _ in test]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # For the purpose of this script, we treat the last 10 rows as 'test'
        # and mask their goal columns.
        train_data = rows[:-10]
        test_data = []
        for row in rows[-10:]:
            new_row = []
            for i, val in enumerate(row):
                if header[i].endswith('-') or header[i].endswith('+'):
                    new_row.append("?")
                else:
                    new_row.append(val)
            test_data.append(new_row)
            
        estimates = guess(header, train_data, test_data)
        
        print("Estimates for the first goal column (Cost-):")
        for i, val in enumerate(estimates):
            print(f"Test row {i+1}: {val:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
