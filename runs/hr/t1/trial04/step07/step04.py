import csv

def flow(header, row, seen):
    """
    Decides if the current employee needs a 'what would keep you here' conversation.
    We prioritize employees who have high 'YearsAtCompany+' but are currently
    showing signs of attrition risk (e.g., low JobSatisfaction or high OverTime).
    
    Strategy: If this is the first row, accept it. Otherwise, compare the current
    row's 'YearsAtCompany+' against the average of 'seen' rows. If the current
    row has a high tenure but low satisfaction, flag them for retention.
    """
    # Identify indices
    try:
        tenure_idx = header.index('YearsAtCompany+')
        sat_idx = header.index('JobSatisfaction')
        ot_idx = header.index('overTime')
    except ValueError:
        return False

    # If no history, accept the first one
    if not seen:
        return True

    # Extract current values
    current_tenure = row[tenure_idx]
    current_sat = row[sat_idx]
    current_ot = row[ot_idx]

    # Calculate baseline from seen data
    seen_tenures = [s[tenure_idx] for s in seen if isinstance(s[tenure_idx], (int, float))]
    if not seen_tenures:
        return False
    
    avg_tenure = sum(seen_tenures) / len(seen_tenures)

    # Logic: Flag if they are a long-tenured employee (above average) 
    # who is either dissatisfied or working overtime.
    is_long_tenure = current_tenure > avg_tenure
    is_at_risk = (current_sat < 3) or (current_ot == 'Yes')

    return is_long_tenure and is_at_risk

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

    # Simulate the flow
    seen = []
    flagged_count = 0
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)

    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Employees identified for retention conversation: {flagged_count}")
    print("Strategy: Targeted long-tenured employees (above average) showing signs of dissatisfaction or overtime.")
