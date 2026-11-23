import csv

def flow(header, row, seen):
    """
    Decides if the current employee needs a 'what would keep you here' conversation.
    We target employees who are high-performers or long-tenured but might be at risk.
    Using a Secretary Problem-inspired approach: we observe the first 20% of 
    employees to establish a baseline for 'YearsAtCompany+' and then pick the 
    first one that exceeds that baseline.
    """
    # Identify indices
    try:
        years_idx = header.index('YearsAtCompany+')
    except ValueError:
        return False

    # If this is the first row, we can't compare
    if not seen:
        return False

    # Calculate baseline from seen data (first 20% or all if fewer)
    n = len(seen)
    limit = max(1, 800 // 5)
    
    # If we are in the observation phase, don't pick
    if n < limit:
        return False
    
    # Calculate the max 'YearsAtCompany+' seen so far as our threshold
    threshold = max(r[years_idx] for r in seen)
    
    # If current row exceeds the threshold, flag for conversation
    if row[years_idx] > threshold:
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
    selected_count = 0
    for row in rows:
        if flow(header, row, seen):
            selected_count += 1
        seen.append(row)
        
    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Employees flagged for 'what would keep you here' conversation: {selected_count}")
    print("Strategy: Flagging employees who exceed the tenure baseline established by the first 20% of the stream.")
