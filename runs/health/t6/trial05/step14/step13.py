import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # The customer asks about the "two built-in rules".
    # In the context of this dataset (which uses 'criterion' as a symbolic input),
    # we compare the performance (ydist) of the two most common criteria:
    # 'absolute_error' vs 'squared_error'.
    
    crit_idx = header.index('criterion')
    
    # Create a table to calculate ydist
    tbl = ezr.Tbl(all_data)
    
    # Group ydist by criterion
    ydists_abs = [ezr.ydist(tbl, r) for r in rows if r[crit_idx] == 'absolute_error']
    ydists_sq = [ezr.ydist(tbl, r) for r in rows if r[crit_idx] == 'squared_error']
    
    # Run the certification
    is_same = certify(ydists_abs, ydists_sq)
    
    print("Analysis: Does the choice of 'criterion' make a real difference?")
    print(f"Mean ydist for 'absolute_error': {sum(ydists_abs)/len(ydists_abs):.4f}")
    print(f"Mean ydist for 'squared_error': {sum(ydists_sq)/len(ydists_sq):.4f}")
    
    if is_same:
        print("Result: The difference is statistically insignificant. You can stop arguing about it.")
    else:
        print("Result: The difference is statistically significant. The choice of criterion matters.")
