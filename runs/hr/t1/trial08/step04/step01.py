import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    'YearsAtCompany+' is a goal to maximize.
    We return the indices of the top 5% of rows based on this metric.
    """
    # Identify the index for 'YearsAtCompany+'
    target_col = "YearsAtCompany+"
    idx = header.index(target_col)
    
    # Create list of (value, original_index)
    data = []
    for i, row in enumerate(rows):
        data.append((row[idx], i))
    
    # Sort by YearsAtCompany+ descending
    data.sort(key=lambda x: x[0], reverse=True)
    
    # Calculate 5% limit (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    
    # Return the indices of the top performers
    return [item[1] for item in data[:limit]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = None
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns (starting with uppercase) to float
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
            
    indices = remember(header, rows)
    
    print("Staff members who stay unusually long (Top 5% by YearsAtCompany+):")
    print(f"{'Index':<10} | {'YearsAtCompany':<15} | {'JobRole'}")
    print("-" * 45)
    
    role_idx = header.index('jobRole')
    years_idx = header.index('YearsAtCompany+')
    
    for i in indices:
        print(f"{i:<10} | {rows[i][years_idx]:<15} | {rows[i][role_idx]}")
