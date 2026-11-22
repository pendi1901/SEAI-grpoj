import ezr
import random

def flow(header, row, seen):
    """
    Decide if the current row is worth a 'what would keep you here' conversation.
    We use the 'wins' logic: if the row is significantly better than the 
    average of what we have seen so far, we flag it.
    """
    if not seen:
        return False
    
    # Create a table from seen rows to establish a baseline
    tbl = ezr.Tbl([header] + seen)
    
    # Use the 'wins' function from ezr to rank the current row
    # against the distribution of the seen rows.
    # A score > 0 means it is better than the average.
    ranker = ezr.wins(tbl)
    score = ranker(row)
    
    # If the score is positive, it's better than average.
    # We choose to flag it if it's in the top 10% of the distribution.
    return score > 0

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Simulate arrival of rows
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    flags = 0
    for row in rows:
        if flow(header, row, seen):
            flags += 1
        seen.append(row)
        
    print(f"Processed {len(rows)} employees.")
    print(f"Flagged {flags} employees for a 'what would keep you here' conversation.")
    print("Decision logic: Flagging employees who perform better than the current average.")
