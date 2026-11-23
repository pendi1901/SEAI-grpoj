import csv
import step02

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics.
    We use a simple hill-climbing heuristic: try each lever, 
    estimate the goal value using KNN (from step02), and pick the best change.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    # Load data to provide context for KNN estimation
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_data = next(reader)
        for r in reader:
            processed_row = []
            for i, val in enumerate(r):
                if header_data[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    best_recommendation = {}
    best_val = -float('inf') if is_maximize else float('inf')
    
    # Try each lever
    for col, allowed in levers.items():
        col_idx = header.index(col)
        original_val = row[col_idx]
        
        # Test potential values
        options = allowed if isinstance(allowed, list) else [allowed[0], allowed[1]]
        
        for val in options:
            if val == original_val:
                continue
                
            test_row = list(row)
            test_row[col_idx] = val
            
            # Estimate goal using KNN
            prediction = step02.guess(header, rows, [test_row])[0]
            
            if (is_maximize and prediction > best_val) or (not is_maximize and prediction < best_val):
                best_val = prediction
                best_recommendation = {col: val}
                
    return best_recommendation

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

    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'StockOptionLevel': (0, 3)
    }

    # Example: Fix a row that might be considered 'bad' (e.g., low tenure)
    # We pick the first row as a sample
    bad_row = rows[0]
    recommendation = fix(header, bad_row, levers)
    
    print("Since there is no budget for pay increases, we recommend the following changes to improve retention:")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to '{val}'")
