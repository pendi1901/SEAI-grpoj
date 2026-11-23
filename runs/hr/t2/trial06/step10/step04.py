import csv
import step01
import step03

def flow(header, row, seen):
    """
    Decides if the current row needs a 'what would keep you here' conversation.
    We identify employees with low tenure (YearsAtCompany+) compared to the 
    average of the 'seen' population, suggesting they are at risk of leaving.
    """
    tenure_idx = header.index('YearsAtCompany+')
    
    # If this is the first row, we can't compare, so let it go
    if not seen:
        return False
    
    # Calculate average tenure of seen employees
    tenures = [r[tenure_idx] for r in seen]
    avg_tenure = sum(tenures) / len(tenures)
    
    # If current employee's tenure is significantly lower than the average 
    # (e.g., less than 50% of the average), flag for retention conversation.
    # We use a threshold to ensure we don't flag everyone.
    if row[tenure_idx] < (0.5 * avg_tenure):
        return True
    
    return False

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
            
    # Simulate the arrival process
    seen = []
    flagged_count = 0
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
        
    print("Retention Analysis Report:")
    print(f"Processed {len(rows)} employee records.")
    print(f"Identified {flagged_count} employees who may need a 'what would keep you here' conversation.")
    print("Criteria: Employees with tenure significantly below the running average of the group.")
