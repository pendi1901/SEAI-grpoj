import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the top 10% of rows with the highest ydist.
    We then compare the distribution of input values in these 'worst' rows
    against the rest of the data using the tree-based split logic.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = [(ezr.ydist(tbl, r), r) for r in rows]
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Define worst as the top 10%
    n_worst = max(1, len(rows) // 10)
    worst_rows = [x[1] for x in scored[:n_worst]]
    
    # We look for columns that show high variance or specific values 
    # in the worst rows compared to the global population.
    # A simple approach: find the column that, when split, 
    # most effectively isolates the 'worst' rows.
    best_col = None
    max_diff = -1
    
    # Only consider input columns (not goals)
    input_cols = [c for c in tbl.x]
    
    for col in input_cols:
        # Calculate mean of this column in worst rows vs all rows
        vals_worst = [r[col.at] for r in worst_rows if r[col.at] != "?"]
        if not vals_worst: continue
        
        mu_worst = sum(vals_worst) / len(vals_worst)
        mu_all = col.mu
        
        # The 'blame' is the column where the worst rows deviate most from the mean
        diff = abs(mu_worst - mu_all)
        if diff > max_diff:
            max_diff = diff
            best_col = col.txt
            
    return [best_col] if best_col else []

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    blamed_cols = blame(header, rows)
    
    print("Analysis: Why do our worst setups leave people waiting?")
    if blamed_cols:
        print(f"The primary factor identified is: {blamed_cols[0]}")
        print("This column shows the most significant deviation in the worst-performing configurations.")
    else:
        print("No single factor could be isolated.")
        
    exit(0)
