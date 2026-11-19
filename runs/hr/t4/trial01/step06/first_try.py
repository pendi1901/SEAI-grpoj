import csv
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the goal column for the given row and calculates its rank
    relative to the existing rows.
    """
    # Identify goal column
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    # Create a copy of the row to fill in the goal
    test_row = list(row)
    
    # Use step02 logic to predict the goal
    # We pass the full dataset as training, and the single row as test
    prediction = guess(header, rows, [test_row])[0]
    
    # Compare prediction against all rows
    all_goals = [r[goal_idx] for r in rows]
    
    if is_maximize:
        better_count = sum(1 for g in all_goals if prediction > g)
    else:
        better_count = sum(1 for g in all_goals if prediction < g)
        
    p = better_count / len(all_goals)
    
    reason = (f"This team arrangement is estimated to be better than {p:.1%} "
              f"of existing records in terms of {header[goal_idx].strip('+-')}.")
    
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
            
    # Example: Take the last row, hide its goal, and justify it
    test_row = list(rows[-1])
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows[:-1], test_row)
    
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
