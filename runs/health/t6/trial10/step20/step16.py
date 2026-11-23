import ezr
import step02
import step06

def justify(header, rows, row):
    """
    Justifies why a 'biggest, deepest' setup might not be optimal.
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason explains that bigger/deeper does not always mean better.
    """
    # Use the logic from step06 to estimate performance and calculate p
    p, _ = step06.justify(header, rows, row)
    
    # Identify the index of Max_depth and N_estimators to reference in the reason
    # The customer asked about "biggest, deepest"
    reason = (f"This configuration is better than {p:.2f} of all known setups; "
              "bigger and deeper models often overfit or add unnecessary complexity "
              "without improving multi-objective performance.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Simulate a "biggest, deepest" setup (e.g., high N_estimators, high Max_depth)
    # We pick a row that has high values for these to represent the customer's query
    idx_n = header.index("N_estimators")
    idx_d = header.index("Max_depth")
    
    # Find a row that is "big and deep"
    big_rows = [r for r in rows if r[idx_n] > 150 and r[idx_d] > 10]
    test_row = list(big_rows[0] if big_rows else rows[0])
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Analysis of 'biggest, deepest' setup:")
    print(f"Justification: {reason}")
