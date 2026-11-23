import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
        
        # The customer asks about the "two built-in rules".
        # In the context of the provided code and dataset, we compare
        # the performance of the two primary split criteria used in the tree:
        # 'absolute_error' vs 'squared_error' (the two most common in the data).
        
        crit_idx = header.index("criterion")
        
        # Extract MRE- (index 0) for rows using different criteria
        abs_err_rows = [r[0] for r in rows if r[crit_idx] == "absolute_error"]
        sq_err_rows = [r[0] for r in rows if r[crit_idx] == "squared_error"]
        
        # Perform the certification
        is_same = certify(abs_err_rows, sq_err_rows)
        
        print(f"Comparing MRE- for {len(abs_err_rows)} 'absolute_error' setups vs {len(sq_err_rows)} 'squared_error' setups.")
        if is_same:
            print("Conclusion: The choice of criterion makes no real difference; it is just noise.")
        else:
            print("Conclusion: The choice of criterion results in a statistically significant difference.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    
    exit(0)
