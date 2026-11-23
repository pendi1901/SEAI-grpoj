import csv

def spot(header, rows):
    """
    Identifies rows that contain suspicious data.
    We look for input values that are statistically unlikely (outliers) 
    compared to the rest of the dataset. We use the Interquartile Range (IQR) 
    method on numeric columns to flag rows with extreme values.
    """
    suspicious_scores = {}
    
    # Identify numeric input columns (exclude goals)
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
    
    for idx in numeric_indices:
        # Extract valid numeric data for this column
        col_data = [row[idx] for row in rows if isinstance(row[idx], (int, float))]
        if not col_data:
            continue
            
        # Calculate IQR
        col_data.sort()
        q1 = col_data[len(col_data) // 4]
        q3 = col_data[3 * len(col_data) // 4]
        iqr = q3 - q1
        
        # Define bounds (1.5 * IQR rule)
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Flag rows that fall outside the bounds
        for i, row in enumerate(rows):
            val = row[idx]
            if isinstance(val, (int, float)):
                if val < lower_bound or val > upper_bound:
                    # Increment suspicion score for this row
                    suspicious_scores[i] = suspicious_scores.get(i, 0) + 1
                    
    # Sort rows by suspicion score (number of outliers found) descending
    sorted_rows = sorted(suspicious_scores.items(), key=lambda x: x[1], reverse=True)
    
    return [item[0] for item in sorted_rows]

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
            
    suspicious_indices = spot(header, rows)
    
    print("Trust Analysis: Rows with suspicious input data")
    print(f"We identified {len(suspicious_indices)} rows that contain values significantly "
          "outside the normal range for our employees.")
    print("Estimates for these rows may be unreliable due to anomalous input data.")
    print("\nTop 5 most suspicious row indices:")
    for idx in suspicious_indices[:5]:
        print(f"- Row index {idx}")
    
    print("\nLogic: Rows were flagged based on statistical outliers (IQR method) "
          "across numeric input fields. If a new hire's data resembles these "
          "outliers, our model's predictions will be less trustworthy.")
