import csv

def flow(header, row, seen):
    """
    Decide if the current employee needs a 'what would keep you here' conversation.
    We prioritize employees who have high tenure (YearsAtCompany+) but are 
    potentially at risk (e.g., high overtime, low job satisfaction).
    
    Since we cannot revisit the pile, we use a threshold based on the 
    distribution of the 'seen' data to decide if the current row is 
    'unusually valuable' or 'at risk'.
    """
    idx_years = header.index('YearsAtCompany+')
    idx_overtime = header.index('overTime')
    idx_satisfaction = header.index('JobSatisfaction')
    
    # Current row values
    current_years = row[idx_years]
    current_ot = row[idx_overtime]
    current_sat = row[idx_satisfaction]
    
    # If this is the first row, we can't compare, so we wait
    if not seen:
        return False
    
    # Calculate thresholds from seen data
    seen_years = [r[idx_years] for r in seen]
    avg_years = sum(seen_years) / len(seen_years)
    
    # Logic: Target long-tenured employees (above average) 
    # who are working overtime or have low job satisfaction.
    is_long_tenure = current_years > avg_years
    is_at_risk = (current_ot == 'Yes') or (current_sat <= 2)
    
    # If they are a long-term asset and showing signs of risk, 
    # flag them for a conversation.
    if is_long_tenure and is_at_risk:
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
    
    seen = []
    flags = 0
    for row in rows:
        if flow(header, row, seen):
            flags += 1
        seen.append(row)
    
    print(f"Analysis complete. Out of {len(rows)} employees, {flags} were flagged for a 'what would keep you here' conversation.")
