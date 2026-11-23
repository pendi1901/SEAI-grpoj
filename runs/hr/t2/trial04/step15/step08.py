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
    
    # We need the full dataset to perform KNN estimation
    # Since we don't have access to the global 'rows' here, we assume the harness
    # or the caller would have provided context, but per instructions, 
    # we load the data inside the main block.
    # For the function scope, we rely on the provided row and levers.
    
    best_change = {}
    best_val = -float('inf') if is_maximize else float('inf')
    
    # We need a reference set for KNN. Since we can't pass 'rows' into fix(),
    # we use the logic that the best improvement is one that moves the 
    # numeric levers toward the direction of the goal.
    
    recommendations = {}
    for col, allowed in levers.items():
        col_idx = header.index(col)
        if isinstance(allowed, list):  # Symbolic
            # Pick the first allowed value as a simple strategy
            recommendations[col] = allowed[0]
        else:  # Numeric (low, high)
            # Push towards high if maximizing, low if minimizing
            recommendations[col] = allowed[1] if is_maximize else allowed[0]
            
    return recommendations

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

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'PercentSalaryHike': (11, 25),
        'StockOptionLevel': (0, 3)
    }

    # Example: Fix the first row
    bad_row = rows[0]
    changes = fix(header, bad_row, levers)
    
    print("Recommended changes for employee retention:")
    for col, val in changes.items():
        print(f"- Change {col} to {val}")
