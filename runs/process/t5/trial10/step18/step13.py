import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (same apart from noise), False if they are significantly different.
    Uses the same() function from ezr.stats.
    """
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # The customer asks if results shifted after a change in how teams decide what to build.
    # We simulate this by splitting the data into two halves:
    # 'Before' (first half) and 'After' (second half).
    # We compare the performance (ydist) of these two groups.
    
    tbl = ezr.Tbl(data)
    n = len(rows)
    mid = n // 2
    
    # Calculate ydist for all rows
    # A row is better when its goals are closer to their best (0 for -, 1 for +).
    # Lower ydist is better.
    before_ydists = [ezr.ydist(tbl, rows[i]) for i in range(mid)]
    after_ydists = [ezr.ydist(tbl, rows[i]) for i in range(mid, n)]
    
    # Perform the certification
    is_same = certify(before_ydists, after_ydists)
    
    print("Analysis: Did the results shift after the change in team decision-making?")
    print(f"Before change (n={len(before_ydists)}), mean ydist: {sum(before_ydists)/len(before_ydists):.4f}")
    print(f"After change (n={len(after_ydists)}), mean ydist: {sum(after_ydists)/len(after_ydists):.4f}")
    
    if is_same:
        print("Result: The difference in performance is statistically insignificant.")
        print("Conclusion: The results are effectively the same as before.")
    else:
        print("Result: The difference in performance is statistically significant.")
        print("Conclusion: The results have genuinely shifted.")
