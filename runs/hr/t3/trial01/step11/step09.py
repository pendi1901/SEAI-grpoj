import csv

def spot(header, rows):
    """
    Identifies suspicious rows by checking for logical inconsistencies.
    
    Common HR data entry errors:
    1. YearsAtCompany < YearsInCurrentRole (Impossible)
    2. YearsAtCompany < YearsSinceLastPromotion (Impossible)
    3. YearsInCurrentRole < YearsSinceLastPromotion (Often suspicious)
    4. TotalWorkingYears < YearsAtCompany (Impossible)
    """
    suspicious = []
    
    # Map column names to indices
    idx_map = {name: i for i, name in enumerate(header)}
    
    # Indices for logic checks
    c_years = idx_map['YearsAtCompany+']
    c_role = idx_map['YearsInCurrentRole+']
    c_promo = idx_map['YearsSinceLastPromotion']
    c_total = idx_map['TotalWorkingYears']
    
    for i, row in enumerate(rows):
        score = 0
        
        # Logic: Years at company must be >= years in current role
        if row[c_years] < row[c_role]:
            score += 3
            
        # Logic: Years at company must be >= years since last promotion
        if row[c_years] < row[c_promo]:
            score += 3
            
        # Logic: Total working years must be >= years at company
        if row[c_total] < row[c_years]:
            score += 2
            
        # Logic: Years in current role must be >= years since last promotion
        if row[c_role] < row[c_promo]:
            score += 1
            
        if score > 0:
            suspicious.append((i, score))
            
    # Sort by score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[1], reverse=True)
    
    return [item[0] for item in suspicious]

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspects = spot(header, rows)
    
    print("Data Integrity Analysis: Suspicious Records Found")
    print(f"Total suspicious rows identified: {len(suspects)}")
    print("Top 5 most suspicious row indices:")
    for idx in suspects[:5]:
        print(f"- Row {idx}")
        
    print("\nLogic: Flagged rows where tenure metrics are logically inconsistent (e.g., YearsAtCompany < YearsInCurrentRole).")
