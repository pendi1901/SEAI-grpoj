import ezr
import random

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    """
    # Use the stats functions from ezr to check for differences
    # same() checks cliffs delta and KS test, and optionally Cohen's d
    return ezr.same(xs, ys, eps=0.35)

def analyze_setups(header, rows):
    """
    Compare the accuracy (MRE-) of 'big' setups vs 'small' setups.
    'Big' is defined as having N_estimators > median.
    """
    # Create table to get column indices
    tbl = ezr.Tbl([header] + rows)
    
    # Find index for N_estimators and MRE-
    n_est_idx = header.index('N_estimators')
    mre_idx = header.index('MRE-')
    
    # Get all N_estimators values to find the median
    n_vals = [r[n_est_idx] for r in rows]
    median_n = sorted(n_vals)[len(n_vals) // 2]
    
    # Split rows into big and small
    big = [r[mre_idx] for r in rows if r[n_est_idx] > median_n]
    small = [r[mre_idx] for r in rows if r[n_est_idx] <= median_n]
    
    return big, small

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        data = list(ezr.csv(filename))
        header = data[0]
        rows = data[1:]
        
        big, small = analyze_setups(header, rows)
        
        is_same = certify(big, small)
        
        print("Analysis: Comparing MRE- for 'big' vs 'small' setups.")
        print(f"Big setups (N_estimators > median): {len(big)} rows, mean MRE: {sum(big)/len(big):.4f}")
        print(f"Small setups (N_estimators <= median): {len(small)} rows, mean MRE: {sum(small)/len(small):.4f}")
        
        if is_same:
            print("\nConclusion: The difference in accuracy is not statistically significant. It is likely noise.")
        else:
            print("\nConclusion: The difference in accuracy is statistically significant. The setup size matters.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    
    exit(0)
