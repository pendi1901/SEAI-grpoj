import ezr
import step03

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    """
    return step03.certify(xs, ys)

def compare_rules(header, rows):
    """
    Compares the performance of the two primary ways to rank rows:
    1. The default tree-based ranker (ezr.ranker).
    2. The distance-based ranker (ezr.ydist).
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Rule 1: Tree-based ranker (as defined in ezr.ranker)
    # This builds a tree and uses leaf means to rank
    ranker_func = ezr.ranker(tbl)
    scores_tree = [ranker_func(r) for r in rows]
    
    # Rule 2: Distance-based ranker (ydist)
    # This ranks directly by how close the row is to the ideal goals
    scores_dist = [ezr.ydist(tbl, r) for r in rows]
    
    # We compare the distributions of these scores to see if the 
    # ranking logic produces significantly different results.
    return certify(scores_tree, scores_dist)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    is_same = compare_rules(header, rows)
    
    print("Comparing the tree-based ranker vs the distance-based ranker.")
    if is_same:
        print("Conclusion: The choice between the two rules makes no real difference.")
        print("The results are statistically indistinguishable.")
    else:
        print("Conclusion: The choice between the two rules makes a real difference.")
        print("The ranking methods produce statistically significant different results.")
