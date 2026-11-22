import csv

def flow(header, row, seen):
    """
    Decides if the current employee needs a 'what would keep you here' conversation.
    Strategy: Identify 'high-value' employees who are at risk of attrition.
    We look for employees with high 'YearsAtCompany+' (tenure) and 
    'JobSatisfaction' who are currently 'No' for 'attrition' but might be 
    approaching a threshold where they could leave.
    
    If the current row's 'YearsAtCompany+' is in the top 10% of the 'seen' 
    data and they have high 'JobSatisfaction', we flag them.
    """
    years_idx = header.index('YearsAtCompany+')
    sat_idx = header.index('JobSatisfaction')
    attrition_idx = header.index('attrition')
    
    # If this is the first row, we can't compare, so let it go
    if not seen:
        return False
    
    # Extract tenure of seen employees
    seen_years = [r[years_idx] for r in seen]
    threshold = sorted(seen_years, reverse=True)[max(0, int(len(seen) * 0.1))]
    
    current_years = row[years_idx]
    current_sat = row[sat_idx]
    current_attrition = row[attrition_idx]
    
    # Logic: If they are a long-tenured employee (top 10%) with high satisfaction
    # but we want to ensure they stay (proactive retention), flag them.
    if current_years >= threshold and current_sat >= 3 and current_attrition == 'No':
        return True
    
    return False

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
    
    # Simulate the stream
    seen = []
    flagged_count = 0
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
    
    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Employees identified for 'what would keep you here' conversation: {flagged_count}")
    print("Strategy: Flagged high-tenure, high-satisfaction employees for proactive retention.")
