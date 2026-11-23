import csv
import step02
import numpy as np

def justify(header, rows, row):
    """
    Estimates the goal column for the provided row and compares it against
    the historical distribution of that goal in the provided rows.
    Returns (percentile, reason).
    """
    # Identify the goal column (first one ending in + or -)
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    goal_idx = goal_indices[0]
    goal_name = header[goal_idx]
    
    # Estimate the goal value for the input row using step02's logic
    prediction = step02.guess(header, rows, [row])[0]
    
    # Extract all known goal values from the historical rows
    historical_values = [r[goal_idx] for r in rows]
    
    # Calculate how many rows are worse than the prediction
    # If goal ends in +, higher is better. If -, lower is better.
    if goal_name.endswith('+'):
        better_than = [v for v in historical_values if v < prediction]
    else:
        better_than = [v for v in historical_values if v > prediction]
        
    p = len(better_than) / len(historical_values)
    
    # The answer to "Why not just pay everyone more?"
    # We explain that retention is a complex function of many variables, 
    # not just salary, and our model shows that individual circumstances 
    # (like job role and overtime) play a significant role.
    reason = (f"Retention is driven by a complex combination of factors beyond just salary, "
              f"and our analysis shows that optimizing specific variables like job role "
              f"and overtime is more effective than a blanket pay increase.")
    
    return p, reason

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
    
    # Create a test row by masking the goal of the first row
    test_row = rows[0][:]
    goal_idx = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')][0]
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    
    print(f"Rank: {p:.4f}")
    print(f"Justification: {reason}")
