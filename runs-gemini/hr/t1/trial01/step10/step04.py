import csv

def flow(header, row, seen):
    """
    Decides if the current employee needs a 'what would keep you here' conversation.
    We prioritize employees who have high 'YearsAtCompany+' but are currently
    experiencing 'OverTime' (Yes) or low 'JobSatisfaction', as these are 
    indicators of potential attrition for high-tenure staff.
    
    This is an online decision problem: we compare the current row against 
    the distribution of the 'seen' rows.
    """
    # Indices for decision criteria
    try:
        tenure_idx = header.index("YearsAtCompany+")
        ot_idx = header.index("overTime")
        sat_idx = header.index("JobSatisfaction")
    except ValueError:
        return False

    # If this is the first row, we can't compare, so let it go
    if not seen:
        return False

    # Extract current values
    curr_tenure = float(row[tenure_idx])
    curr_ot = row[ot_idx]
    curr_sat = float(row[sat_idx])

    # Calculate statistics from 'seen' to define 'high tenure' and 'low satisfaction'
    tenures = [float(r[tenure_idx]) for r in seen]
    sats = [float(r[sat_idx]) for r in seen]
    
    avg_tenure = sum(tenures) / len(tenures)
    avg_sat = sum(sats) / len(sats)

    # Logic: If they have been here longer than average AND (they work overtime OR 
    # have lower than average job satisfaction), they are a priority for retention.
    if curr_tenure > avg_tenure:
        if curr_ot == "Yes" or curr_sat < avg_sat:
            return True

    return False

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    rows = []
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

    seen = []
    triggered = 0
    for row in rows:
        if flow(header, row, seen):
            triggered += 1
        seen.append(row)

    print(f"Retention Analysis Complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Number of employees flagged for 'what would keep you here' conversation: {triggered}")
    print("The model flags high-tenure employees who are currently working overtime or report low job satisfaction.")
