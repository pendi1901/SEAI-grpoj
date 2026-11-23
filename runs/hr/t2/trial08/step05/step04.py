import csv
import step01

def flow(header, row, seen):
    """
    Decide if the current employee needs a 'what would keep you here' conversation.
    We identify employees who are 'unusually long' in their tenure (top 5%)
    compared to the 'seen' population.
    """
    goal_col = "YearsAtCompany+"
    idx = header.index(goal_col)
    
    # If this is the first row, we can't compare, so return False
    if not seen:
        return False
    
    # Get all previous tenure values
    tenures = [r[idx] for r in seen if isinstance(r[idx], (int, float))]
    if not tenures:
        return False
    
    # Define 'unusually long' as being in the top 5% of the current distribution
    # or simply higher than the current average.
    # Given the constraint to stop on a choice, we look for high performers.
    avg_tenure = sum(tenures) / len(tenures)
    
    # If the current employee's tenure is significantly higher than the average
    # of those seen so far, flag them for a retention conversation.
    if row[idx] > (avg_tenure * 1.5):
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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Simulate the flow
    seen = []
    retention_candidates = 0
    for row in rows:
        if flow(header, row, seen):
            retention_candidates += 1
        seen.append(row)
    
    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Employees identified for 'what would keep you here' conversation: {retention_candidates}")
    print("Strategy: Flagging employees with tenure 50% higher than the running average.")
