import csv
from step01 import remember

def guess(header, train, test):
    """
    Estimates the first goal column for test rows by finding the 
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
            v1, v2 = float(row1[i]), float(row2[i])
            d += (v1 - v2) ** 2
        return d ** 0.5

    results = []
    for t_row in test:
        # Find the row in train that is closest to t_row
        best_match = min(train, key=lambda r: dist(r, t_row))
        results.append(float(best_match[goal_idx]))
    
    return results

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            all_rows = [row for row in reader]
            
        # Split data: use first 700 for training, last 100 for testing
        train = all_rows[:700]
        test_raw = all_rows[700:]
        
        # Mask the goals in the test set to simulate "?"
        test_masked = []
        for row in test_raw:
            new_row = [val if not (header[i].endswith('-') or header[i].endswith('+')) else "?" 
                       for i, val in enumerate(row)]
            test_masked.append(new_row)
            
        predictions = guess(header, train, test_masked)
        
        # Calculate average prediction for the customer
        avg_cost = sum(predictions) / len(predictions)
        
        print("Customer Inquiry: Estimated Cost and Idle Time")
        print(f"Based on analysis of {len(train)} training records:")
        print(f"The estimated average value for the first goal column ('{header[8]}') is: {avg_cost:.4f}")
        print("This estimate is derived from nearest-neighbor matching on input parameters.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
