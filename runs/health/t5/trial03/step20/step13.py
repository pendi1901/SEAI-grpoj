import ezr
import random

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they are significantly different.
    """
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # The customer asks about the "two built-in rules".
    # In the context of this dataset and the provided ezr library, 
    # we compare the two primary ways to rank rows:
    # 1. The 'tree' ranker (based on decision tree leaves)
    # 2. The 'wins' ranker (based on distance to ideal)
    
    tbl = ezr.Tbl(data)
    
    # Generate rankings using both methods
    ranker_tree = ezr.ranker(tbl)
    ranker_wins = ezr.wins(tbl)
    
    scores_tree = [ranker_tree(r) for r in rows]
    scores_wins = [ranker_wins(r) for r in rows]
    
    # Check if the rankings are statistically the same
    is_same = certify(sorted(scores_tree), sorted(scores_wins))
    
    print("Analysis: Does the choice between the two built-in ranking rules make a difference?")
    if is_same:
        print("Result: The difference between the two rules is statistically insignificant.")
        print("You can stop arguing about it; both rules yield effectively the same results.")
    else:
        print("Result: There is a statistically significant difference between the two rules.")
        print("The choice of rule does matter for this dataset.")
    
    print(f"\nMean score (Tree): {sum(scores_tree)/len(scores_tree):.4f}")
    print(f"Mean score (Wins): {sum(scores_wins)/len(scores_wins):.4f}")
