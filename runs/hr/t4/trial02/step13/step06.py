import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the goal value for the given row and compares it against
    the distribution of the full dataset to determine its rank.
    """
    # Identify goal column
    goal_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]
    goal_idx = header.index(goal_col)
    
    # Prepare training data
    train_rows = [r for r in rows if r[goal_idx] != "?"]
    
    # Estimate the goal value for the input row using the guess function
    # Note: guess() handles the encoding internally using pandas/LabelEncoder
    prediction = guess(header, train_rows, [row])[0]
    
    # Calculate rank (fraction of rows that 'row' is better than)
    # Better means higher for '+' and lower for '-'
    all_goals = [float(r[goal_idx]) for r in train_rows]
    
    if goal_col.endswith('+'):
        better_than = [g for g in all_goals if prediction > g]
    else:
        better_than = [g for g in all_goals if prediction < g]
        
    p = len(better_than) / len(all_goals)
    
    reason = f"This team's arrangement is estimated to perform better than {p*100:.1f}% of the existing teams regarding {goal_col.strip('+-')}."
    
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
    
    # Test with the last row as a sample
    test_row = rows[-1][:]
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
