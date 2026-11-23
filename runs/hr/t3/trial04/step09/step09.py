import csv

def spot(header, rows):
    """
    Identify rows that contain suspicious data.
    We look for logical inconsistencies:
    1. YearsInCurrentRole > YearsAtCompany
    2. YearsWithCurrManager > YearsAtCompany
    3. YearsSinceLastPromotion > YearsAtCompany
    4. TotalWorkingYears < YearsAtCompany
    """
    suspicious = []
    
    # Map column names to indices
    idx_at_company = header.index('YearsAtCompany+')
    idx_in_role = header.index('YearsInCurrentRole+')
    idx_with_manager = header.index('YearsWithCurrManager+')
    idx_since_promo = header.index('YearsSinceLastPromotion')
    idx_total_work = header.index('TotalWorkingYears')
    
    for i, row in enumerate(rows):
        score = 0
        
        # Logical checks
        if row[idx_in_role] > row[idx_at_company]:
            score += 1
        if row[idx_with_manager] > row[idx_at_company]:
            score += 1
        if row[idx_since_promo] > row[idx_at_company]:
            score += 1
        if row[idx_total_work] < row[idx_at_company]:
            score += 1
            
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
            
    suspects = spot(header, rows)
    
    print(f"Analysis complete. Found {len(suspects)} rows with potentially erroneous data.")
    print("Top 5 most suspicious rows (logical inconsistencies in tenure/role history):")
    for idx in suspects[:5]:
        row = rows[idx]
        print(f"- Row {idx}: YearsAtCompany={row[header.index('YearsAtCompany+')]}, "
              f"TotalWorkingYears={row[header.index('TotalWorkingYears')]}, "
              f"YearsInCurrentRole={row[header.index('YearsInCurrentRole+')]} "
              f"(Check for data entry errors)")
