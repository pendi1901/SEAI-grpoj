import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    'YearsAtCompany+' is a goal to maximize.
    We calculate the 95th percentile of 'YearsAtCompany+' and return
    the indices of rows that meet or exceed this threshold.
    """
    # Identify index for 'YearsAtCompany+'
    idx = header.index('YearsAtCompany+')
    
    # Extract values
    years = [row[idx] for row in rows]
    
    # Calculate threshold for "unusually long" (top 5%)
    sorted_years = sorted(years, reverse=True)
    limit = max(1, len(rows) // 20)
    threshold = sorted_years[limit - 1]
    
    # Find indices of rows meeting the criteria
    best_indices = [i for i, val in enumerate(years) if val >= threshold]
    
    # Ensure we return at most 5% (the logic above naturally fits this)
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
    
    print(f"Identified {len(indices)} employees with unusually long tenure.")
    print("Working arrangements for these employees:")
    
    # Print relevant columns for the identified rows
    cols_to_show = ['businessTravel', 'department', 'jobRole', 'YearsAtCompany+']
    col_indices = [header.index(c) for c in cols_to_show]
    
    for idx in indices:
        details = [str(rows[idx][i]) for i in col_indices]
        print(f" - {', '.join(details)}")
