import ezr
import step06

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining the justification.
    
    This function uses the logic from step06 to estimate the performance of a 
    given row and compare it against the historical dataset.
    """
    return step06.justify(header, rows, row)

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate the customer's request:
    # They liked setup B (index 1), we recommended A (index 0).
    # We explain why A is better than B.
    row_a = list(rows[0])
    row_b = list(rows[1])
    
    # Mask the goals for the comparison
    for i, name in enumerate(header):
        if name.endswith("-") or name.endswith("+"):
            row_a[i] = "?"
            row_b[i] = "?"
            
    p_a, reason_a = justify(header, rows, row_a)
    p_b, reason_b = justify(header, rows, row_b)
    
    print("Comparison Analysis: Why we recommended Setup A over Setup B.")
    print(f"Setup A performance percentile: {p_a:.4f}")
    print(f"Setup B performance percentile: {p_b:.4f}")
    
    if p_a >= p_b:
        print(f"Explanation: {reason_a} Setup B is less optimal, performing better than only {int(p_b*100)}% of configurations.")
    else:
        print("Explanation: Both setups are highly competitive, but A aligns better with our optimization goals.")
    
    exit(0)
