import csv

def spot(header, rows):
    """
    Identifies rows that contain suspicious data.
    We look for logical inconsistencies:
    1. YearsInCurrentRole > YearsAtCompany
    2. YearsWithCurrManager > YearsAtCompany
    3. YearsSinceLastPromotion > YearsAtCompany
    4. TotalWorkingYears < YearsAtCompany
    5. Age < (TotalWorkingYears + 16) (Assuming minimum working age of 16)
    """
    suspicious = []
    
    # Map column names to indices
    idx_at_company = header.index('YearsAtCompany+')
    idx_in_role = header.index('YearsInCurrentRole+')
    idx_with_manager = header.index('YearsWithCurrManager+')
    idx_since_promo = header.index('YearsSinceLastPromotion')
    idx_total_work = header.index('TotalWorkingYears')
    idx_age = header.index('Age')
    
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
        # Age check: A person cannot have worked more years than their age minus 16
        if row[idx_age] < (row[idx_total_work] + 16):
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
    
    print("Analysis: Identifying records that are logically inconsistent.")
    print(f"Found {len(suspects)} records that may be unreliable due to data entry errors.")
    print("When hiring someone unlike anyone else, our estimates are based on historical patterns.")
    print("If the input data for a new hire contains logical contradictions (e.g., more years in a role")
    print("than at the company), our model's predictions cannot be trusted.")
    
    if suspects:
        print(f"\nExample of a suspicious record: Row {suspects[0]}")
        print("These records should be audited before relying on model output for new hires.")
