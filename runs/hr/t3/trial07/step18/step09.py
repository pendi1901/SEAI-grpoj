import csv

def spot(header, rows):
    """
    Identifies rows that look suspicious based on internal consistency.
    We look for rows where numeric values are extreme outliers compared to 
    the rest of the dataset (e.g., Age > 100, YearsAtCompany > TotalWorkingYears).
    """
    suspicious = []
    
    # Indices for sanity checks
    try:
        age_idx = header.index('Age')
        years_comp_idx = header.index('YearsAtCompany+')
        total_years_idx = header.index('TotalWorkingYears')
        years_role_idx = header.index('YearsInCurrentRole+')
    except ValueError:
        return []

    for i, row in enumerate(rows):
        score = 0
        
        # Rule 1: Age sanity check (e.g., Age < 18 or > 90)
        if row[age_idx] < 18 or row[age_idx] > 90:
            score += 5
            
        # Rule 2: YearsAtCompany cannot exceed TotalWorkingYears
        if row[years_comp_idx] > row[total_years_idx]:
            score += 10
            
        # Rule 3: YearsInCurrentRole cannot exceed YearsAtCompany
        if row[years_role_idx] > row[years_comp_idx]:
            score += 8
            
        # Rule 4: StandardHours is usually 80 in this dataset
        std_hours_idx = header.index('StandardHours')
        if row[std_hours_idx] != 80:
            score += 3
            
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspects = spot(header, rows)
    
    print("Suspicious rows identified (most suspicious first):")
    for idx in suspects[:10]:  # Print top 10
        print(f"Row {idx} has internal data inconsistencies.")
    
    if not suspects:
        print("No suspicious rows found.")
