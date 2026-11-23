import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    We look for rows where 'YearsAtCompany+' is in the top 5% of the dataset.
    """
    # Identify index for the goal column
    target_col = "YearsAtCompany+"
    idx = header.index(target_col)
    
    # Extract values and track original indices
    data = []
    for i, row in enumerate(rows):
        val = row[idx]
        data.append((val, i))
    
    # Sort by YearsAtCompany+ descending (higher is better/longer stay)
    data.sort(key=lambda x: x[0], reverse=True)
    
    # Calculate 5% limit
    limit = max(1, len(rows) // 20)
    
    # Return the indices of the top 5%
    return [item[1] for item in data[:limit]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns (starting with uppercase) to float
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    best_indices = remember(header, rows)
    
    print("Staff members who stay unusually long (Top 5% by YearsAtCompany+):")
    print(f"{'Index':<10} | {'YearsAtCompany':<15} | {'JobRole'}")
    print("-" * 45)
    
    role_idx = header.index('jobRole')
    years_idx = header.index('YearsAtCompany+')
    
    for idx in best_indices:
        print(f"{idx:<10} | {rows[idx][years_idx]:<15} | {rows[idx][role_idx]}")
