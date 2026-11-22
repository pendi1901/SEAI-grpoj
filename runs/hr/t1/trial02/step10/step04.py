import csv

def flow(header, row, seen):
    """
    Decides if the current employee needs a 'what would keep you here' conversation.
    We identify employees at risk of attrition (low tenure/satisfaction) 
    compared to the 'seen' population.
    """
    # Identify indices
    try:
        yac_idx = header.index('YearsAtCompany+')
        sat_idx = header.index('JobSatisfaction')
        ot_idx = header.index('overTime')
    except ValueError:
        return False

    # If no history, we can't compare, so default to False
    if not seen:
        return False

    # Current employee metrics
    current_yac = row[yac_idx]
    current_sat = row[sat_idx]
    current_ot = row[ot_idx]

    # Calculate averages from seen data to establish a baseline
    seen_yac = [r[yac_idx] for r in seen]
    seen_sat = [r[sat_idx] for r in seen]
    
    avg_yac = sum(seen_yac) / len(seen_yac)
    avg_sat = sum(seen_sat) / len(seen_sat)

    # Logic: If the employee has lower-than-average tenure, 
    # lower-than-average satisfaction, and works overtime, 
    # they are a high-priority candidate for retention.
    is_low_tenure = current_yac < avg_yac
    is_low_sat = current_sat < avg_sat
    is_overworked = (current_ot == 'Yes')

    return is_low_tenure and is_low_sat and is_overworked

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

    # Simulate the arrival process
    seen = []
    conversations_needed = 0
    for row in rows:
        if flow(header, row, seen):
            conversations_needed += 1
        seen.append(row)

    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Recommended 'what would keep you here' conversations: {conversations_needed}")
