import ezr

def blame(header, rows):
    """
    Identifies input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the 'worst' rows 
    against the 'best' rows. Columns where the distributions differ 
    significantly are the ones 'doing the damage'.
    """
    # Create a table to handle column metadata and normalization
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (ascending: best to worst)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Define 'best' and 'worst' as the top and bottom 20%
    n = len(sorted_rows) // 5
    best = sorted_rows[:n]
    worst = sorted_rows[-n:]
    
    # We look for input columns (x) where the distribution in 'worst' 
    # is significantly different from 'best'.
    # We use the 'same' function from ezr which checks for statistical difference.
    suspects = []
    for col in tbl.x:
        at = col.at
        # Extract values for this column
        vals_best = [r[at] for r in best if r[at] != "?"]
        vals_worst = [r[at] for r in worst if r[at] != "?"]
        
        # If the distributions are NOT the same, this column is a suspect
        if not ezr.same(vals_best, vals_worst):
            suspects.append(header[at])
            
    return suspects

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Identify the culprits
    culprits = blame(header, rows)
    
    print("Customer Query: Why do the bad setups miss so badly? Which settings are doing the damage?")
    if culprits:
        print(f"Analysis: The following settings are significantly correlated with poor performance: {', '.join(culprits)}.")
        print("These parameters show a statistically different distribution in the worst-performing setups compared to the best.")
    else:
        print("Analysis: No single input setting clearly explains the poor performance; the damage may be due to complex interactions.")
    
    exit(0)
