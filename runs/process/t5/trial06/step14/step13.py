import ezr
import random

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable,
    False if they are significantly different.
    Uses the same logic as ezr.same, which checks for statistical 
    significance using Cliff's Delta and the Kolmogorov-Smirnov test.
    """
    return ezr.same(xs, ys)

def analyze():
    """
    Compares the performance (ydist) of the first half of the data 
    (pre-change) vs the second half (post-change).
    """
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Create a table to calculate ydist
    tbl = ezr.Tbl(data)
    
    # Split data into two halves
    mid = len(rows) // 2
    pre_change = rows[:mid]
    post_change = rows[mid:]
    
    # Calculate ydist for each group
    pre_ydists = [ezr.ydist(tbl, r) for r in pre_change]
    post_ydists = [ezr.ydist(tbl, r) for r in post_change]
    
    # Perform the certification
    is_same = certify(pre_ydists, post_ydists)
    
    print("--- Analysis: Did the results shift after the spring change? ---")
    print(f"Pre-change sample size:  {len(pre_ydists)}")
    print(f"Post-change sample size: {len(post_ydists)}")
    print(f"Pre-change avg ydist:    {sum(pre_ydists)/len(pre_ydists):.4f}")
    print(f"Post-change avg ydist:   {sum(post_ydists)/len(post_ydists):.4f}")
    print(f"Are the distributions statistically the same? {is_same}")
    
    if not is_same:
        print("Conclusion: The results have shifted significantly.")
    else:
        print("Conclusion: The results are statistically the same; any difference is noise.")

if __name__ == "__main__":
    analyze()
    exit(0)
