import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining why 'row' is better or worse than 
    the average configuration.
    """
    # Create a table to handle normalization and distance
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Estimate the goals for the input row using the tree-based ranker
    # The ranker returns a function that estimates ydist
    ranker_func = ezr.ranker(tbl)
    estimated_ydist = ranker_func(row)
    
    # Calculate ydist for all existing rows to compare
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # p is the fraction of rows that have a higher (worse) ydist than our estimate
    # (i.e., our row is better than them)
    better_than_count = sum(1 for d in all_ydists if d > estimated_ydist)
    p = better_than_count / len(rows)
    
    # Construct a reason based on the performance rank
    if p > 0.7:
        reason = f"This setup is highly efficient, outperforming {int(p*100)}% of configurations."
    elif p > 0.4:
        reason = f"This setup performs reasonably well, better than {int(p*100)}% of configurations."
    else:
        reason = f"This setup is suboptimal, performing better than only {int(p*100)}% of configurations."
    
    return p, reason

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a random row to justify, mask its goals
    test_row = list(rows[random.randint(0, len(rows) - 1)])
    for i in range(len(header)):
        if header[i].endswith(("-", "+")):
            test_row[i] = "?"
            
    # Get justification
    p, reason = justify(header, rows, test_row)
    
    print("--- Justification Analysis ---")
    print(f"Performance Rank (p): {p:.4f}")
    print(f"Reasoning: {reason}")
    
    exit(0)
