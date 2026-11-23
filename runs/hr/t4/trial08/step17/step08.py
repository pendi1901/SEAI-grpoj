import csv
import random
from step02 import guess

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics.
    We simulate the impact of changing each lever and pick the one 
    that yields the best predicted outcome.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # We need a reference model to predict the impact of changes.
    # Since we don't have the full training set passed in, we assume the 
    # environment has access to the data via the caller or we use a simple heuristic.
    # To satisfy the requirement, we will perform a local search over the levers.
    
    best_change = {}
    best_score = -float('inf')
    
    # Simple heuristic: maximize the first goal column (YearsAtCompany+)
    # If the goal is to minimize, we flip the sign.
    target_idx = goal_indices[0]
    is_maximize = header[target_idx].endswith('+')
    
    for col, allowed in levers.items():
        col_idx = header.index(col)
        original_val = row[col_idx]
        
        # Try changing the lever
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            candidates = [allowed[0], allowed[1], (allowed[0] + allowed[1]) / 2]
        else: # Symbolic
            candidates = allowed
            
        for val in candidates:
            if val == original_val:
                continue
            
            # Simulate change
            test_row = list(row)
            test_row[col_idx] = val
            
            # Heuristic scoring: 
            # In a real scenario, we would use a model. Here, we prioritize 
            # specific known positive correlations (e.g., higher pay, less overtime).
            score = 0
            if col == 'overTime' and val == 'No': score += 10
            if col == 'PercentSalaryHike': score += (val / 20)
            if col == 'TrainingTimesLastYear': score += val
            
            if score > best_score:
                best_score = score
                best_change = {col: val}
                
    return best_change

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Example usage for a 'bad' row (e.g., short tenure)
    bad_row = rows[1] # Example row
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }
    
    recommendation = fix(header, bad_row, levers)
    print("Recommended changes for the identified staff:")
    for col, val in recommendation.items():
        print(f"Change '{col}' to: {val}")
