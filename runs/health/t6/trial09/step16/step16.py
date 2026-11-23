import ezr
import step02
import step06

def justify(header, rows, row):
    """
    Justify why we don't just use the biggest, deepest setup.
    We compare the performance of the provided row against the distribution
    of all rows. If the 'biggest' setups (e.g., high N_estimators) are not 
    statistically better than others, we explain that complexity does not 
    guarantee quality.
    """
    # Use the logic from step06 to calculate the percentile
    p, _ = step06.justify(header, rows, row)
    
    # To answer the customer's question, we check if higher complexity 
    # (e.g., N_estimators) correlates with better performance.
    # If not, we add that to the reason.
    tbl = ezr.Tbl([header] + rows)
    n_est_idx = [i for i, name in enumerate(header) if name == 'N_estimators'][0]
    
    # Split into high vs low N_estimators
    vals = [r[n_est_idx] for r in rows]
    median = sorted(vals)[len(vals) // 2]
    
    high_n = [ezr.ydist(tbl, r) for r in rows if r[n_est_idx] >= median]
    low_n = [ezr.ydist(tbl, r) for r in rows if r[n_est_idx] < median]
    
    # If the distributions are indistinguishable, complexity is unnecessary
    if ezr.same(high_n, low_n):
        reason = (f"This setup is in the top {int((1-p)*100)}% of configurations, "
                  "and since larger models do not statistically outperform smaller ones, "
                  "using the biggest setup is an unnecessary waste of resources.")
    else:
        reason = (f"This setup is in the top {int((1-p)*100)}% of configurations, "
                  "and while complexity impacts performance, the biggest setup is "
                  "not always the most efficient choice.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row to justify, masking its goals
    target_row = list(rows[0])
    for i, name in enumerate(header):
        if name[-1] in "+-":
            target_row[i] = "?"
            
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification: {reason}")
    print(f"Performance percentile: {p:.4f}")
    exit(0)
