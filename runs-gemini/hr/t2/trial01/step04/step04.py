import csv
import step01
import step02
import step03

def flow(header, row, seen):
    """
    Decides if the current employee needs a 'what would keep you here' conversation.
    We identify 'at-risk' employees as those with low tenure compared to the 
    average of the historical data (the 'seen' rows).
    """
    # Identify goal columns (those ending in +)
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+')]
    if not goal_indices:
        return False
    
    # Use the first goal column: YearsAtCompany+
    target_idx = goal_indices[0]
    
    # If this is the first row, we have no baseline, so don't trigger
    if not seen:
        return False
    
    # Calculate baseline from seen data
    tenures = [r[target_idx] for r in seen if isinstance(r[target_idx], (int, float))]
    if not tenures:
        return False
    
    avg_tenure = sum(tenures) / len(tenures)
    
    # Current employee's tenure
    current_val = row[target_idx]
    
    # If current tenure is significantly lower than the average of those seen,
    # flag them for a retention conversation.
    return current_val < (avg_tenure * 0.5)

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
    flags = 0
    for row in rows:
        if flow(header, row, seen):
            flags += 1
        seen.append(row)
    
    print(f"Analysis complete. Total employees processed: {len(rows)}")
    print(f"Number of employees flagged for retention conversation: {flags}")
