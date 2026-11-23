import csv

def spot(header, rows):
    """
    Identifies suspicious rows by checking for logical inconsistencies 
    between related columns (e.g., YearsInCurrentRole > TotalWorkingYears).
    """
    # Indices for columns that have logical dependencies
    try:
        yicr_idx = header.index('YearsInCurrentRole+')
        twy_idx = header.index('TotalWorkingYears')
        yac_idx = header.index('YearsAtCompany+')
        yssp_idx = header.index('YearsSinceLastPromotion')
        ywcm_idx = header.index('YearsWithCurrManager+')
    except ValueError:
        return []

    suspicious = []
    for i, row in enumerate(rows):
        score = 0
        
        # Rule 1: Years in current role cannot exceed total working years
        if row[yicr_idx] > row[twy_idx]:
            score += 10
            
        # Rule 2: Years at company cannot be less than years in current role
        if row[yac_idx] < row[yicr_idx]:
            score += 5
            
        # Rule 3: Years since last promotion cannot exceed total working years
        if row[yssp_idx] > row[twy_idx]:
            score += 8
            
        # Rule 4: Years with current manager cannot exceed years at company
        if row[ywcm_idx] > row[yac_idx]:
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspects = spot(header, rows)
    
    print("Suspicious records identified (Logical inconsistencies found):")
    for idx in suspects[:10]:  # Print top 10
        print(f"- Row {idx} has conflicting tenure data.")
    
    if not suspects:
        print("No suspicious records found.")
    else:
        print(f"\nTotal of {len(suspects)} records flagged for manual review.")
