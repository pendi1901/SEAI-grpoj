import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable
    (i.e., the difference is likely just noise). Returns False if they differ.
    """
    # We use the same logic as the stats layer in ezr.py
    # same() checks cliffs and ks tests.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    # The customer asks about the choice between two built-in rules.
    # In the context of this dataset, we compare two common configurations:
    # 'absolute_error' vs 'squared_error' for the 'criterion' column (index 4).
    
    crit_idx = 4
    mre_idx = 0
    
    abs_error_mres = [row[mre_idx] for row in rows if row[crit_idx] == "absolute_error"]
    sq_error_mres = [row[mre_idx] for row in rows if row[crit_idx] == "squared_error"]
    
    # Run the certification
    is_same = certify(abs_error_mres, sq_error_mres)
    
    print("Analysis: Does the choice of 'criterion' (absolute vs squared error) matter?")
    if is_same:
        print("Result: The difference in performance is likely just noise.")
        print("Conclusion: You can stop arguing about it; the choice makes no real difference.")
    else:
        print("Result: There is a statistically significant difference in performance.")
        print("Conclusion: The choice of criterion does matter.")
        
    print(f"\nAverage MRE for 'absolute_error': {sum(abs_error_mres)/len(abs_error_mres):.4f}")
    print(f"Average MRE for 'squared_error':  {sum(sq_error_mres)/len(sq_error_mres):.4f}")
    
    exit(0)
