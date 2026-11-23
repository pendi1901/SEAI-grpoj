import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import step02

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    To answer the customer's question, we simulate the 'Sales' department
    with 'overTime' set to 'No'.
    """
    # Create copies to avoid modifying original data
    train_df = pd.DataFrame(train, columns=header)
    test_df = pd.DataFrame(test, columns=header)
    
    # Identify goal column
    goal_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]
    
    # Apply the customer's hypothetical: If department is Sales, set overTime to 'No'
    # We apply this to the test set to see the predicted impact
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    
    for i in range(len(test_df)):
        if test_df.iloc[i, dept_idx] == 'Sales':
            test_df.iloc[i, ot_idx] = 'No'
            
    # Convert back to list format for step02.guess
    train_processed = train_df.values.tolist()
    test_processed = test_df.values.tolist()
    
    return step02.guess(header, train_processed, test_processed)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    # Prepare data
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    
    # Train on full dataset, test on Sales employees
    train_data = rows
    test_data = [list(r) for r in rows if r[header.index('department')] == 'Sales']
    
    # Mask goals
    for r in test_data:
        r[goal_idx] = "?"
        
    predictions = guess(header, train_data, test_data)
    
    avg_pred = sum(predictions) / len(predictions)
    print("Analysis: If we cut overtime across Sales, what happens to tenure?")
    print(f"Predicted average 'YearsAtCompany+' for Sales staff (with no overtime): {avg_pred:.2f} years.")
    print("This estimate is based on a Random Forest model trained on the provided HR dataset.")
