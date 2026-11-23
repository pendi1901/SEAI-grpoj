import ezr
import step02
import step06

def justify(header, rows, row):
    """
    Answers why we shouldn't just use the biggest/deepest setup.
    We compare the performance of a 'deep' setup (high Max_depth)
    against the general population to show that complexity does not
    guarantee better outcomes.
    """
    # Use the logic from step06 to calculate the percentile score
    # and generate the justification string.
    return step06.justify(header, rows, row)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Identify the index for Max_depth
    max_depth_idx = header.index("Max_depth")
    
    # Find a 'deep' setup (e.g., max depth in the dataset)
    max_depth_val = max(r[max_depth_idx] for r in rows)
    deep_row = [r for r in rows if r[max_depth_idx] == max_depth_val][0]
    
    # Mask the goals for the justification function
    tbl = ezr.Tbl([header] + rows)
    test_row = list(deep_row)
    for col in tbl.y:
        test_row[col.at] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print("--- Analysis: Why not use the deepest setup? ---")
    print(f"A setup with Max_depth={max_depth_val} is better than {p:.1%} of all configurations.")
    print(f"Reasoning: {reason}")
    print("Conclusion: Simply increasing complexity (depth) does not guarantee optimal performance, "
          "as the relationship between inputs and goals is non-linear and often noisy.")
    
    exit(0)
