import csv
import step01

def flow(header, row, seen):
    """
    Decides whether to trigger a 'what would keep you here' conversation.
    We target employees who are high-performers (based on YearsAtCompany+)
    but might be at risk. We use a simple threshold: if the current row's
    'YearsAtCompany+' is in the top 5% of the 'seen' data, we flag it.
    """
    years_idx = header.index('YearsAtCompany+')
    
    # If this is the first row, we can't compare, so let it pass
    if not seen:
        return False
    
    # Extract historical 'YearsAtCompany+' values
    history = [r[years_idx] for r in seen if isinstance(r[years_idx], (int, float))]
    
    if not history:
        return False
    
    # Define threshold as the 95th percentile of seen data
    history.sort()
    threshold = history[int(len(history) * 0.95)]
    
    # If current employee has stayed longer than 95% of previous staff,
    # they are a valuable long-term asset worth retaining.
    current_val = row[years_idx]
    if isinstance(current_val, (int, float)) and current_val >= threshold:
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Simulate the arrival process
    seen = []
    triggered_count = 0
    for row in rows:
        if flow(header, row, seen):
            triggered_count += 1
        seen.append(row)
    
    print("Retention Conversation Analysis:")
    print(f"Processed {len(rows)} employees.")
    print(f"Triggered 'what would keep you here' conversations for {triggered_count} employees.")
    print("Logic: Flagged employees who have stayed longer than 95% of their peers.")
