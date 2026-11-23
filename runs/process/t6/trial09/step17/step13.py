import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable,
    False if they are significantly different.
    Uses the same logic as step03 which leverages ezr.same.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    # The customer asks if results shifted after a change in how teams decide what to build.
    # We interpret this as comparing the first half of the data (pre-change)
    # against the second half (post-change).
    # We use the primary goal 'Cost-' (index 9) as the performance metric.
    mid = len(rows) // 2
    pre_change = [r[9] for r in rows[:mid] if r[9] != "?"]
    post_change = [r[9] for r in rows[mid:] if r[9] != "?"]
    
    is_same = certify(pre_change, post_change)
    
    print("Analysis: Did the team's decision-making change shift performance?")
    if is_same:
        print("Result: The difference is statistically insignificant (it was likely luck).")
    else:
        print("Result: The difference is statistically significant (it is real).")
        
    print(f"Pre-change mean cost: {sum(pre_change)/len(pre_change):.4f}")
    print(f"Post-change mean cost: {sum(post_change)/len(post_change):.4f}")
    
    exit(0)
