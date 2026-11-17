import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that `row` is better than,
    and a sentence explaining why the row is considered good.
    """
    # Create a table to handle the distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    # ydist measures how far a row is from the ideal (0.0 is perfect)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate ydist for the target row
    # We need to fill in the '?' goals to calculate distance.
    # We use the median of the column as a neutral estimate for the missing goals.
    filled_row = list(row)
    for i, val in enumerate(filled_row):
        if val == "?":
            filled_row[i] = ezr.mid(tbl.cols[i])
            
    target_ydist = ezr.ydist(tbl, filled_row)
    
    # Calculate how many rows are worse (have a higher ydist) than our target
    worse_count = sum(1 for d in all_ydists if d > target_ydist)
    p = worse_count / len(rows)
    
    # Generate a reason based on the performance
    reason = (f"This setup is in the top {int((1-p)*100)}% of all configurations "
              f"evaluated, achieving a performance distance of {target_ydist:.3f} "
              "relative to the ideal target.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Pick a random row to justify
    random.seed(1234567891)
    target_row = random.choice(rows)
    
    # Mask the goals to simulate the customer's request
    masked_row = [target_row[i] if not header[i].endswith(('-', '+')) else "?" 
                  for i in range(len(target_row))]
    
    p, reason = justify(header, rows, masked_row)
    
    print("Justification Analysis:")
    print(f"Target Row: {masked_row}")
    print(f"Percentile: {p:.2%}")
    print(f"Reason: {reason}")
    
    exit(0)
