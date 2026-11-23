import csv

def flow(header, row, seen):
    """
    Decides if the current employee needs a 'what would keep you here' conversation.
    Strategy: We look for employees who are 'high value' (long tenure) but might 
    be at risk of attrition. Since we cannot go back, we use a threshold based 
    on the distribution of the 'seen' data to identify top performers/tenured staff.
    """
    idx_years = header.index('YearsAtCompany+')
    idx_attrition = header.index('attrition')
    
    # If we haven't seen enough data, be conservative
    if len(seen) < 50:
        return False
    
    # Calculate the threshold for 'long tenure' based on what we have seen so far
    tenures = [r[idx_years] for r in seen]
    threshold = sum(tenures) / len(tenures)
    
    # If the current employee has stayed longer than the average of those seen,
    # they are a candidate for a retention conversation.
    if row[idx_years] > threshold:
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
    
    # Simulate the flow
    seen = []
    triggered = 0
    for row in rows:
        if flow(header, row, seen):
            triggered += 1
        seen.append(row)
        
    print(f"Retention Analysis Complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Retention conversations recommended: {triggered}")
    print("Logic: Employees with tenure significantly above the running average are flagged.")
