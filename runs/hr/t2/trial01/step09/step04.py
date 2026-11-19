import csv
import step01

def flow(header, row, seen):
    """
    Decides if the current row is a candidate for a 'what would keep you here' 
    conversation. We define this as being in the top 5% of tenure (using 
    the logic from step01) compared to the history of 'seen' rows.
    """
    if not seen:
        return False
    
    # Combine seen rows with current row to evaluate relative standing
    all_rows = seen + [row]
    
    # Use step01 logic to find top 5% indices
    best_indices = step01.remember(header, all_rows)
    
    # If the current row (the last one) is in the top 5%, trigger conversation
    return (len(all_rows) - 1) in best_indices

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
    triggered_count = 0
    for row in rows:
        if flow(header, row, seen):
            triggered_count += 1
        seen.append(row)
    
    print("Retention Conversation Analysis:")
    print(f"Total employees processed: {len(rows)}")
    print(f"Conversations recommended: {triggered_count}")
    print("Logic: Triggered for employees in the top 5% of tenure (YearsAtCompany+, YearsInCurrentRole+, YearsWithCurrManager+).")
