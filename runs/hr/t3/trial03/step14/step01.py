import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    'YearsAtCompany+' is a goal to maximize.
    We calculate the 95th percentile of 'YearsAtCompany+' and return
    the indices of rows that meet or exceed this threshold.
    """
    # Identify index for 'YearsAtCompany+'
    try:
        idx = header.index('YearsAtCompany+')
    except ValueError:
        return [0]

    # Extract all values for the goal column
    years = [row[idx] for row in rows]
    
    # Calculate threshold for "unusually long" (top 5%)
    sorted_years = sorted(years, reverse=True)
    limit = max(1, len(rows) // 20)
    threshold = sorted_years[limit - 1]
    
    # Find indices of rows meeting the criteria
    indices = [i for i, val in enumerate(years) if val >= threshold]
    
    # Ensure we return at most 5% of the rows (limit is already 5%)
    return indices[:limit]

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
    idx_years = header.index('YearsAtCompany+')
    for i in best_indices:
        row = rows[i]
        print(f"Row {i}: YearsAtCompany = {row[idx_years]}, "
              f"JobRole = {row[header.index('jobRole')]}, "
              f"Department = {row[header.index('department')]}")
