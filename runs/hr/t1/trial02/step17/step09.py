import csv

def spot(header, rows):
    """
    Identifies suspicious rows by checking for logical inconsistencies
    between related columns (e.g., YearsInCurrentRole > YearsAtCompany).
    """
    h_map = {name: i for i, name in enumerate(header)}
    
    # Indices for logical checks
    yac_idx = h_map.get('YearsAtCompany+')
    yicr_idx = h_map.get('YearsInCurrentRole+')
    ysp_idx = h_map.get('YearsSinceLastPromotion')
    ywcm_idx = h_map.get('YearsWithCurrManager+')
    
    suspicious = []
    
    for idx, row in enumerate(rows):
        score = 0
        
        # Rule 1: Years in current role cannot exceed years at company
        if row[yicr_idx] > row[yac_idx]:
            score += 10
            
        # Rule 2: Years with manager cannot exceed years at company
        if row[ywcm_idx] > row[yac_idx]:
            score += 10
            
        # Rule 3: Years since last promotion cannot exceed years at company
        if row[ysp_idx] > row[yac_idx]:
            score += 5
            
        # Rule 4: TotalWorkingYears should be >= YearsAtCompany
        if 'TotalWorkingYears' in h_map:
            if row[h_map['TotalWorkingYears']] < row[yac_idx]:
                score += 5
        
        if score > 0:
            suspicious.append((score, idx))
            
    # Sort by score descending
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspect_indices = spot(header, rows)
    
    print(f"Found {len(suspect_indices)} potentially erroneous records.")
    print("Top 5 most suspicious rows (Index: Reason):")
    for idx in suspect_indices[:5]:
        row = rows[idx]
        yac = row[header.index('YearsAtCompany+')]
        yicr = row[header.index('YearsInCurrentRole+')]
        ywcm = row[header.index('YearsWithCurrManager+')]
        
        reason = []
        if yicr > yac: reason.append("Role tenure > Company tenure")
        if ywcm > yac: reason.append("Manager tenure > Company tenure")
        
        print(f"Row {idx}: {', '.join(reason)}")
