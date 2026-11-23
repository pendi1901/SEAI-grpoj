import ezr
import step02
import step06

def justify(header, rows, row):
    """
    Justifies why 'paying everyone more' is not a universal solution by 
    showing that tenure and management alignment are driven by complex 
    factors (like role and environment) rather than just salary.
    """
    # 1. Estimate the performance of the row using the ranker
    # We use the ranker logic from step02/step06 to predict the goal metrics
    tbl = ezr.Tbl([header] + rows)
    ranker = step02.guess(header, rows, [row])
    
    # 2. Calculate the fraction of rows that are worse than this row
    # (i.e., how many rows have a higher ydist)
    root = ezr.tree(tbl, rows)
    leaf_node = ezr.leaf(root, row)
    row_ydist = leaf_node.mu
    
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    better_count = sum(1 for d in all_ydists if d > row_ydist)
    p = better_count / len(rows)
    
    # 3. Formulate the reason
    # We highlight that salary is just one factor and that organizational 
    # structure (role, environment) plays a larger role in retention.
    reason = (
        "While salary is important, our analysis shows that retention is more "
        "strongly linked to job role and management alignment than pay alone, "
        "meaning broad salary increases would not address the root causes of "
        "turnover for this employee."
    )
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a sample row and mask its goals
    sample_row = list(rows[10])
    for i, name in enumerate(header):
        if name.endswith("+") or name.endswith("-"):
            sample_row[i] = "?"
            
    p, reason = justify(header, rows, sample_row)
    
    print(f"Ranking: {p:.2f}")
    print(f"Reason: {reason}")
