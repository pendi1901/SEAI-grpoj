import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is a 'retention risk' candidate.
    We define a risk as someone with low 'YearsAtCompany+' 
    (a goal to maximize) compared to the population seen so far.
    If the row's tenure is significantly below the average of 
    what we have seen, we flag it for a conversation.
    """
    # Identify the goal column
    idx = header.index('YearsAtCompany+')
    
    # If this is the first row, we can't compare, so let it go
    if not seen:
        return False
    
    # Extract seen values for the goal
    tenures = [r[idx] for r in seen if r[idx] != "?"]
    
    # If no data yet, let it go
    if not tenures:
        return False
    
    # Calculate average tenure seen so far
    avg_tenure = sum(tenures) / len(tenures)
    
    # If the current employee's tenure is significantly lower than average
    # (e.g., less than 50% of the average), flag for a conversation.
    # This is a heuristic for "retention risk".
    current_tenure = row[idx]
    if current_tenure != "?" and current_tenure < (avg_tenure * 0.5):
        return True
        
    return False

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate arrival of rows one by one
    seen = []
    flags = 0
    for row in rows:
        if flow(header, row, seen):
            flags += 1
        seen.append(row)
        
    print("Retention Risk Analysis")
    print("-" * 40)
    print(f"Total employees processed: {len(rows)}")
    print(f"Employees flagged for 'what keeps you here' talk: {flags}")
    print("-" * 40)
    print("Logic: Flagged employees with tenure < 50% of the running average.")
