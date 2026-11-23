import csv

def spot(header, rows):
    """
    Identifies suspicious rows by checking for logical inconsistencies 
    between related columns (e.g., YearsAtCompany vs TotalWorkingYears).
    """
    # Indices for columns that should have logical relationships
    try:
        years_at_co_idx = header.index('YearsAtCompany+')
        total_years_idx = header.index('TotalWorkingYears')
        years_in_role_idx = header.index('YearsInCurrentRole+')
        years_with_mgr_idx = header.index('YearsWithCurrManager+')
    except ValueError:
        return []

    suspicious = []
    
    for i, row in enumerate(rows):
        # Rule 1: Years at company cannot exceed total working years
        # Rule 2: Years in current role cannot exceed years at company
        # Rule 3: Years with manager cannot exceed years at company
        
        score = 0
        
        # Check numeric consistency
        if row[years_at_co_idx] > row[total_years_idx]:
            score += 3
        if row[years_in_role_idx] > row[years_at_co_idx]:
            score += 2
        if row[years_with_mgr_idx] > row[years_at_co_idx]:
            score += 2
            
        # Check for impossible values (e.g., negative years)
        if any(row[idx] < 0 for idx in [years_at_co_idx, total_years_idx, years_in_role_idx]):
            score += 5
            
        if score > 0:
            suspicious.append((score, i))
            
    # Sort by score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
    
    print("Suspicious rows identified (logical inconsistencies in tenure data):")
    for idx in suspicious_indices[:10]:
        print(f"Row {idx} is highly suspicious.")
    
    if not suspicious_indices:
        print("No obvious data entry errors found.")
    else:
        print(f"\nTotal of {len(suspicious_indices)} rows flagged for review.")
