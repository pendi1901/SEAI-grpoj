import csv

def spot(header, rows):
    """
    Identifies rows that look 'wrong' based on domain-specific constraints.
    We look for logical inconsistencies in employee data:
    1. YearsInCurrentRole > TotalWorkingYears (Impossible)
    2. YearsWithCurrManager > TotalWorkingYears (Impossible)
    3. YearsSinceLastPromotion > YearsAtCompany (Impossible)
    4. Age < (TotalWorkingYears + 16) (Assuming working age starts at 16)
    """
    idx_map = {name: i for i, name in enumerate(header)}
    suspects = []

    for i, row in enumerate(rows):
        score = 0
        
        # Extract relevant fields
        age = row[idx_map['Age']]
        total_years = row[idx_map['TotalWorkingYears']]
        years_role = row[idx_map['YearsInCurrentRole+']]
        years_manager = row[idx_map['YearsWithCurrManager+']]
        years_company = row[idx_map['YearsAtCompany+']]
        years_promo = row[idx_map['YearsSinceLastPromotion']]

        # Check for logical inconsistencies
        if years_role > total_years:
            score += 3
        if years_manager > total_years:
            score += 3
        if years_promo > years_company:
            score += 2
        if age < (total_years + 16):
            score += 1
            
        if score > 0:
            suspects.append((score, i))

    # Sort by score descending (most suspicious first)
    suspects.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in suspects]

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

    suspect_indices = spot(header, rows)
    
    print("Data Integrity Analysis: Identifying potentially erroneous records.")
    print(f"Found {len(suspect_indices)} rows with logical inconsistencies.")
    print("Top 5 most suspicious row indices:")
    for idx in suspect_indices[:5]:
        print(f"- Row {idx}")
    
    print("\nNote: These rows contain values that violate standard HR logic "
          "(e.g., tenure in role exceeding total working years).")
