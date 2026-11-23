import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is worth a 'what would keep you here' conversation.
    We use the 'holdout' logic: if the current row is significantly better
    than the best seen so far, we flag it.
    """
    # If this is the first row, we can't compare it to anything.
    if not seen:
        return False
    
    # Create a table to use ezr's distance metrics
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the distance of the current row from the ideal goals
    # A lower ydist is better.
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate the distances of all previously seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # If the current row is better than the best row seen so far,
    # we flag it for a conversation.
    # We use a threshold: it must be better than the current best.
    if current_ydist < min(seen_ydists):
        return True
    
    return False

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the arrival of rows one by one
    seen = []
    flags = 0
    
    # We process a subset to demonstrate the flow
    for i, row in enumerate(rows[:100]):
        if flow(header, row, seen):
            flags += 1
            print(f"Row {i}: Flagged for 'what would keep you here' conversation.")
        seen.append(row)
        
    print(f"\nTotal rows processed: 100")
    print(f"Total conversations recommended: {flags}")
    
    exit(0)
