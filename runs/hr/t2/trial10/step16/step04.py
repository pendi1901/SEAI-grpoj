import csv
import step01
import step03

def flow(header, row, seen):
    """
    Decides if the current row is a 'top performer' based on 'YearsAtCompany+'
    compared to the history of seen rows. We use a simple threshold:
    if the current row's tenure is significantly better than the mean of 
    the seen rows (using the logic from step03), we flag it.
    """
    tenure_idx = header.index('YearsAtCompany+')
    current_val = row[tenure_idx]
    
    if not seen:
        return True
    
    seen_vals = [r[tenure_idx] for r in seen if isinstance(r[tenure_idx], (int, float))]
    if not seen_vals:
        return True
        
    mean_seen = sum(seen_vals) / len(seen_vals)
    
    # If the current employee has been here longer than the average of those seen,
    # they are a candidate for a retention conversation.
    return current_val > mean_seen

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

    # Simulate the arrival process
    seen = []
    flagged_count = 0
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
    
    print("Retention Conversation Analysis:")
    print(f"Processed {len(rows)} employees.")
    print(f"Flagged {flagged_count} employees for a 'what would keep you here' conversation.")
    print("Decision logic: Flagged employees with tenure above the historical average.")
