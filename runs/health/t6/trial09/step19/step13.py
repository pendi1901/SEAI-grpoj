import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    return step03.certify(xs, ys)

def compare_rules(header, rows):
    """
    Compares two rules for selecting rows:
    1. 'acquire' (the default model-based active learning)
    2. 'grabs' (random sampling)
    
    We compare the ydist of the results found by both strategies.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Run both strategies to get a set of rows
    # We use the same budget (the.Stop) for both
    rows_acquire = ezr.acquire(tbl, cap=ezr.the.Stop)
    rows_grabs = ezr.grabs(tbl, cap=ezr.the.Stop)
    
    # Calculate ydist for the results of each strategy
    ydists_acquire = [ezr.ydist(tbl, r) for r in rows_acquire]
    ydists_grabs = [ezr.ydist(tbl, r) for r in rows_grabs]
    
    return ydists_acquire, ydists_grabs

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Compare the two rules
    ydists_acquire, ydists_grabs = compare_rules(header, rows)
    
    # Check if they are statistically the same
    is_same = certify(ydists_acquire, ydists_grabs)
    
    print("Comparison of 'acquire' vs 'grabs' rules:")
    print(f"Mean ydist (acquire): {sum(ydists_acquire)/len(ydists_acquire):.4f}")
    print(f"Mean ydist (grabs):   {sum(ydists_grabs)/len(ydists_grabs):.4f}")
    
    if is_same:
        print("Conclusion: The difference between the rules is likely noise. You can stop arguing.")
    else:
        print("Conclusion: The difference between the rules is statistically significant.")
        
    exit(0)
