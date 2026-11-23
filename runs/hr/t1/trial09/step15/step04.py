import csv

def flow(header, row, seen):
    """
    Decides if the current row is a 'high-value' employee who needs a 
    retention conversation. We define this as having a tenure score 
    (sum of '+' columns) significantly higher than the average of 
    previously seen employees.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    
    # Calculate score for the current row
    current_score = sum(row[i] for i in goal_indices)
    
    # If this is the first row, we have no baseline, so we let it go
    if not seen:
        return False
    
    # Calculate average score of seen rows
    seen_scores = [sum(r[i] for i in goal_indices) for r in seen]
    avg_seen = sum(seen_scores) / len(seen_scores)
    
    # If the current employee's tenure score is significantly higher 
    # (e.g., 20% above average), flag them for a conversation.
    # We use a threshold to ensure we don't pick everyone.
    if current_score > (avg_seen * 1.2):
        return True
    
    return False

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    seen = []
    flagged_count = 0
    print("Processing employee reviews...")
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
        
    print(f"Analysis complete.")
    print(f"Total employees reviewed: {len(rows)}")
    print(f"Employees flagged for retention conversation: {flagged_count}")
