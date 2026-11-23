import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    'YearsAtCompany+' is a goal to maximize.
    We return the indices of the top 5% of rows based on this metric.
    """
    # Identify the index for 'YearsAtCompany+'
    target_col = "YearsAtCompany+"
    try:
        idx = header.index(target_col)
    except ValueError:
        return []

    # Create a list of (value, original_index)
    indexed_rows = []
    for i, row in enumerate(rows):
        val = row[idx]
        if isinstance(val, (int, float)):
            indexed_rows.append((val, i))

    # Sort by value descending (maximize)
    indexed_rows.sort(key=lambda x: x[0], reverse=True)

    # Calculate 5% limit (at least 1, at most 5% of total rows)
    n = len(rows)
    limit = max(1, int(n * 0.05))
    
    # Return the indices of the top rows
    return [item[1] for item in indexed_rows[:limit]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns (starting with uppercase) to floats
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

    best_indices = remember(header, rows)
    
    print("Staff members who stay unusually long (Top 5% by YearsAtCompany+):")
    for i in best_indices:
        row = rows[i]
        years_idx = header.index("YearsAtCompany+")
        role_idx = header.index("jobRole")
        print(f"Row {i}: Role={row[role_idx]}, YearsAtCompany={row[years_idx]}")
