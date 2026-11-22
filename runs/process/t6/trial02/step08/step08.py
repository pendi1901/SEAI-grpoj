import ezr
import step01
import step05

def fix(header, row, levers):
    """
    Suggests changes to levers to improve a bad row.
    Finds the most influential 'bad' factors and moves them 
    towards the values seen in the 'best' rows.
    """
    # Load all data to understand the global distribution
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header_data = next(data_gen)
    all_rows = list(data_gen)
    tbl = ezr.Tbl([header_data] + all_rows)

    # Identify which factors are causing the trouble (blame)
    # We use step05 logic to find columns that correlate with poor performance
    bad_factors = step05.blame(header, all_rows)
    
    # Filter bad_factors to only include those in the provided levers
    candidates = [f for f in bad_factors if f in levers]
    if not candidates:
        # Fallback: pick any lever if no specific bad factor is found
        candidates = list(levers.keys())

    # Find the best rows to see what their values look like
    best_indices = step01.remember(header, all_rows)
    best_rows = [all_rows[i] for i in best_indices]

    # Suggest a change for the first available candidate lever
    target_col = candidates[0]
    col_idx = header.index(target_col)
    
    # Calculate the average value of this column in the best rows
    best_vals = [r[col_idx] for r in best_rows if r[col_idx] != "?"]
    avg_best = sum(best_vals) / len(best_vals) if best_vals else 0.5

    # Apply the change based on lever type
    suggestion = {}
    allowed = levers[target_col]
    
    if isinstance(allowed, list):  # Symbolic
        suggestion[target_col] = allowed[0] # Simplest change
    else:  # Numeric (low, high)
        low, high = allowed
        # Clamp the average best value to the allowed range
        suggestion[target_col] = max(low, min(high, avg_best))
        
    return suggestion

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Simulate a "bad" row (e.g., one with high cost)
    # We pick a row with high Cost- (index 9)
    bad_row = max(rows, key=lambda r: r[9])
    
    # Define levers: numeric ranges based on the data
    levers = {
        "Culture": (0, 1),
        "Criticality": (0, 1),
        "Size": (0, 1),
        "Team Size": (0, 1)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Recommendation:")
    print(f"For the current setup, we recommend the following changes:")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to {val:.4f}")
    print("This should help align the project with higher-performing configurations.")
    
    exit(0)
