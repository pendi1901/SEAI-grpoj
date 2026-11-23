import csv

def spot(header, rows):
    """
    Identifies rows that look wrong due to data entry errors.
    We look for logical inconsistencies:
    1. YearsInCurrentRole > YearsAtCompany
    2. YearsWithCurrManager > YearsAtCompany
    3. YearsSinceLastPromotion > YearsAtCompany
    4. TotalWorkingYears < YearsAtCompany
    """
    idx = {name: i for i, name in enumerate(header)}
    suspects = []

    for i, row in enumerate(rows):
        score = 0
        
        # Logical constraints
        years_at = row[idx['YearsAtCompany+']]
        
        if row[idx['YearsInCurrentRole+']] > years_at:
            score += 1
        if row[idx['YearsWithCurrManager+']] > years_at:
            score += 1
        if row[idx['YearsSinceLastPromotion']] > years_at:
            score += 1
        if row[idx['TotalWorkingYears']] < years_at:
            score += 1
            
        # Statistical outliers (e.g., Age vs TotalWorkingYears)
        if row[idx['TotalWorkingYears']] > (row[idx['Age']] - 14):
            score += 1
            
        if score > 0:
            suspects.append((score, i))
            
    # Sort by score descending (most suspicious first)
    suspects.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in suspects]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = None
    
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
            
    suspect_indices = spot(header, rows)
    
    print("Data Integrity Analysis:")
    print(f"Found {len(suspect_indices)} rows with potential data entry errors.")
    print("Top 5 most suspicious rows:")
    for i in suspect_indices[:5]:
        print(f"- Row {i}: Contains logical inconsistencies in tenure or career progression metrics.")
    
    exit(0)
