import ezr
import step03

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    Uses the same logic as step03 (Cohen's d, Cliff's delta, and KS test).
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # The customer asks about the "two built-in rules". 
    # In the context of this data and the provided tools, we compare 
    # the two primary ways to rank/evaluate setups:
    # 1. The 'tree' ranker (used in step02/step12)
    # 2. The 'ydist' metric (used in step01/step04)
    
    tbl = ezr.Tbl([header] + rows)
    
    # Rule 1: Performance via Tree Ranker (predicting ydist)
    # We build a tree and get the leaf means for all rows
    node = ezr.tree(tbl, tbl.rows)
    ranker_scores = [ezr.leaf(node, r).mu for r in rows]
    
    # Rule 2: Performance via raw ydist
    ydist_scores = [ezr.ydist(tbl, r) for r in rows]
    
    # Compare the two distributions
    is_same = certify(ranker_scores, ydist_scores)
    
    print("--- Analysis: Comparing Evaluation Rules ---")
    if is_same:
        print("Result: The two evaluation rules produce statistically indistinguishable results.")
        print("Conclusion: You can stop arguing; the choice between them does not make a real difference.")
    else:
        print("Result: There is a statistically significant difference between the two rules.")
        print("Conclusion: The choice of rule matters for your analysis.")
