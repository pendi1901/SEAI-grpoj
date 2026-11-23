import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    'YearsAtCompany+' is a goal to maximize.
    We calculate the 95th percentile of 'YearsAtCompany+' and return
    the indices of rows that meet or exceed this threshold.
    """
    idx = header.index('YearsAtCompany+')
    years = [row[idx] for row in rows]
    
    # Calculate threshold for "unusually long" (top 5%)
    sorted_years = sorted(years, reverse=True)
    threshold = sorted_years[int(len(rows) * 0.05)]
    
    # Find indices of rows meeting the criteria
    best_indices = [i for i, val in enumerate(years) if val >= threshold]
    
    # Ensure we return at most 5% of the rows (handle ties at the threshold)
    limit = int(len(rows) * 0.05)
    return best_indices[:limit]

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
    
    indices = remember(header, rows)
    
    print("Staff members who stay unusually long (Top 5% by YearsAtCompany+):")
    print(f"{'Index':<10} | {'YearsAtCompany':<15} | {'JobRole':<20}")
    print("-" * 50)
    
    role_idx = header.index('jobRole')
    years_idx = header.index('YearsAtCompany+')
    
    for i in indices:
        print(f"{i:<10} | {rows[i][years_idx]:<15} | {rows[i][role_idx]}")
