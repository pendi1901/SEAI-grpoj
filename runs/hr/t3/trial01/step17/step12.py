import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    This model captures the interaction between 'department', 'overTime', 
    and tenure to answer the customer's question about the impact of 
    cutting overtime in Sales.
    """
    # Identify goal columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_indices[0]
    
    # Identify input columns
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Encode symbolic columns
    encoders = {}
    for i in input_indices:
        if not header[i][0].isupper():
            le = LabelEncoder()
            # Fit on all available data
            all_vals = [str(r[i]) for r in train] + [str(r[i]) for r in test if r[i] != '?']
            le.fit(all_vals)
            encoders[i] = le

    def transform_row(row):
        new_row = []
        for i in input_indices:
            val = row[i]
            if i in encoders:
                new_row.append(float(encoders[i].transform([str(val)])[0]))
            else:
                new_row.append(float(val))
        return new_row

    X_train = [transform_row(row) for row in train]
    y_train = [float(row[target_idx]) for row in train]
    X_test = [transform_row(row) for row in test]
        
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    # To answer the customer: compare Sales employees with Overtime vs without
    # We create a synthetic test set: copy Sales employees and toggle their Overtime
    sales_rows = [r for r in rows if r[header.index('department')] == 'Sales']
    
    # Create two scenarios for the same Sales employees
    test_data_with_ot = [list(r) for r in sales_rows]
    test_data_no_ot = [list(r) for r in sales_rows]
    
    ot_idx = header.index('overTime')
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    
    for r in test_data_with_ot:
        r[ot_idx] = 'Yes'
        r[goal_idx] = '?'
    for r in test_data_no_ot:
        r[ot_idx] = 'No'
        r[goal_idx] = '?'
        
    preds_with = guess(header, rows, test_data_with_ot)
    preds_without = guess(header, rows, test_data_no_ot)
    
    avg_with = sum(preds_with) / len(preds_with)
    avg_without = sum(preds_without) / len(preds_without)
    
    print("Analysis: Impact of cutting Overtime in Sales on 'YearsAtCompany+'")
    print(f"Average predicted tenure with Overtime: {avg_with:.2f} years")
    print(f"Average predicted tenure without Overtime: {avg_without:.2f} years")
    print(f"Difference: {avg_without - avg_with:.2f} years")
    print("Conclusion: Removing overtime in Sales is predicted to " + 
          ("increase" if avg_without > avg_with else "decrease") + 
          " average retention duration.")
