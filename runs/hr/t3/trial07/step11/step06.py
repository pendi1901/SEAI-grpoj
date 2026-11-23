import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the goal columns for the given row and calculates its percentile
    rank against the existing dataset.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # Prepare training data
    X_train = []
    y_train = []
    encoders = {}
    
    # Fit encoders on all data to handle potential unseen categories
    for i in input_indices:
        if isinstance(rows[0][i], str):
            encoders[i] = LabelEncoder()
            col_data = [r[i] for r in rows]
            encoders[i].fit(col_data)
            
    for r in rows:
        processed = []
        for i in input_indices:
            val = r[i]
            if i in encoders:
                processed.append(encoders[i].transform([val])[0])
            else:
                processed.append(val)
        X_train.append(processed)
        
    # We estimate all goals. For this specific dataset, YearsAtCompany+ is the primary.
    # We use the first goal found for the ranking logic.
    target_idx = goal_indices[0]
    y_train = [r[target_idx] for r in rows]
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict for the input row
    X_test = []
    for i in input_indices:
        val = row[i]
        if i in encoders:
            X_test.append(encoders[i].transform([val])[0])
        else:
            X_test.append(val)
            
    prediction = model.predict([X_test])[0]
    
    # Calculate percentile: what fraction of rows is this row better than?
    # Better means higher for '+' goals.
    better_count = sum(1 for r in rows if r[target_idx] < prediction)
    p = better_count / len(rows)
    
    reason = f"Based on {header[target_idx]}, this arrangement ranks in the top {100*(1-p):.1f}th percentile of all teams."
    
    return (p, reason)

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
            
    # Test with a sample row (masking the goal)
    sample_row = list(rows[0])
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    sample_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, sample_row)
    print(f"Percentile: {p:.4f}")
    print(f"Reason: {reason}")
