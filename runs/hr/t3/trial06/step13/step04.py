import csv

def flow(header, row, seen):
    """
    Decides if the current row is a candidate for a 'what would keep you here' 
    conversation. We look for employees with high tenure (YearsAtCompany+, 
    YearsWithCurrManager+) who are currently at risk (attrition == 'No' but 
    perhaps have low JobSatisfaction or high OverTime).
    
    Since we cannot go back, we use a threshold approach based on the 
    distribution of the 'seen' data.
    """
    idx_attrition = header.index('attrition')
    idx_satisfaction = header.index('JobSatisfaction')
    idx_overtime = header.index('overTime')
    idx_years_company = header.index('YearsAtCompany+')
    idx_years_manager = header.index('YearsWithCurrManager+')

    # If the person is already leaving, no need for a conversation
    if row[idx_attrition] == 'Yes':
        return False

    # Calculate a 'retention risk' score:
    # High tenure + Low satisfaction + Overtime = High risk of future attrition
    tenure_score = (row[idx_years_company] + row[idx_years_manager])
    sat_score = row[idx_satisfaction]
    ot_penalty = 2 if row[idx_overtime] == 'Yes' else 0
    
    # Risk score: higher is more urgent
    risk_score = (tenure_score * 0.5) - (sat_score * 2) + (ot_penalty * 3)

    if not seen:
        return False

    # Compare against the average risk of those seen so far
    seen_risks = []
    for s in seen:
        s_tenure = (s[idx_years_company] + s[idx_years_manager])
        s_sat = s[idx_satisfaction]
        s_ot = 2 if s[idx_overtime] == 'Yes' else 0
        seen_risks.append((s_tenure * 0.5) - (s_sat * 2) + (s_ot * 3))
    
    avg_risk = sum(seen_risks) / len(seen_risks)

    # If this employee's risk score is significantly higher than the average 
    # of those seen, flag them for a conversation.
    return risk_score > (avg_risk * 1.2)

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
    flagged_count = 0
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)

    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Employees flagged for 'what would keep you here' conversation: {flagged_count}")
    print("Strategy: Flagging high-tenure employees with low job satisfaction and overtime.")
