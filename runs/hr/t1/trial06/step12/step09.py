import csv

def spot(header, rows):
    """
    Identifies suspicious rows by checking for logical inconsistencies 
    between related numeric fields.
    
    Common HR data inconsistencies:
    1. YearsInCurrentRole > TotalWorkingYears
    2. YearsWithCurrManager > TotalWorkingYears
    3. YearsSinceLastPromotion > TotalWorkingYears
    4. YearsAtCompany > TotalWorkingYears
    """
    idx_total = header.index('TotalWorkingYears')
    idx_at_co = header.index('YearsAtCompany+')
    idx_role = header.index('YearsInCurrentRole+')
    idx_promo = header.index('YearsSinceLastPromotion')
    idx_mgr = header.index('YearsWithCurrManager+')

    suspicious = []
    
    for i, row in enumerate(rows):
        score = 0
        # Check if any tenure metric exceeds total career length
        if row[idx_at_co] > row[idx_total]: score += 1
        if row[idx_role] > row[idx_total]: score += 1
        if row[idx_promo] > row[idx_total]: score += 1
        if row[idx_mgr] > row[idx_total]: score += 1
        
        # Also check if role tenure exceeds company tenure
        if row[idx_role] > row[idx_at_co]: score += 1
        
        if score > 0:
            suspicious.append((score, i))
            
    # Sort by score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicious]

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

    suspicious_indices = spot(header, rows)
    
    print("Suspicious rows identified (logical inconsistencies in tenure):")
    if not suspicious_indices:
        print("No suspicious rows found.")
    else:
        for idx in suspicious_indices[:10]:
            print(f"Row {idx} is highly suspicious due to conflicting tenure data.")
