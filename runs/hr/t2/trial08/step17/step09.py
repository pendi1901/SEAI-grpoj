import csv

def spot(header, rows):
    """
    Identifies suspicious rows by checking for logical inconsistencies
    between related numeric fields (e.g., YearsInCurrentRole > TotalWorkingYears).
    """
    suspicious = []
    
    # Indices for logical checks
    try:
        idx_total = header.index('TotalWorkingYears')
        idx_role = header.index('YearsInCurrentRole+')
        idx_company = header.index('YearsAtCompany+')
        idx_manager = header.index('YearsWithCurrManager+')
    except ValueError:
        return []

    for i, row in enumerate(rows):
        # Logic check: Years in role/company cannot exceed total working years
        # Also check if YearsInCurrentRole > YearsAtCompany
        score = 0
        if row[idx_role] > row[idx_total]:
            score += 3
        if row[idx_company] > row[idx_total]:
            score += 2
        if row[idx_manager] > row[idx_company]:
            score += 1
            
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
            
    suspects = spot(header, rows)
    
    print("Suspicious records identified (logical inconsistencies in tenure):")
    for i in suspects[:10]:
        row = rows[i]
        print(f"Row {i}: TotalWorkingYears={row[header.index('TotalWorkingYears')]}, "
              f"YearsInCurrentRole={row[header.index('YearsInCurrentRole+')]}, "
              f"YearsAtCompany={row[header.index('YearsAtCompany+')]}")
