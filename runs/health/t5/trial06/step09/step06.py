import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a human-readable explanation.
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # 1. Estimate the goals for the target row
    # We use the tree-based ranker to predict the performance of the row
    # based on its input columns.
    ranker = ezr.ranker(tbl)
    
    # The ranker returns a score (lower ydist is better).
    # Since the row has '?' in goal columns, we use the ranker to estimate its ydist.
    estimated_ydist = ranker(row)
    
    # 2. Compare against all other rows
    # Calculate ydist for all known rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Count how many rows are worse (have a higher ydist) than our estimated row
    # A row is better if its ydist is lower.
    worse_count = sum(1 for d in all_ydists if d > estimated_ydist)
    p = worse_count / len(rows)
    
    # 3. Formulate the reason
    # Identify the most influential input column to explain 'why'
    # We look for the column that splits the tree at the top level
    root_node = ezr.tree(tbl, rows)
    reason = "This configuration is estimated to be better than " + \
             f"{p:.1%} of all known setups, primarily because its " + \
             f"'{header[root_node.at]}' value of {row[root_node.at]} " + \
             "places it in a high-performing region of the decision space."
             
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals to simulate the user's query
    target_row = list(rows[0])
    for i, col_name in enumerate(header):
        if col_name[-1] in "+-":
            target_row[i] = "?"
            
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification for the selected setup:")
    print(reason)
    
    exit(0)
