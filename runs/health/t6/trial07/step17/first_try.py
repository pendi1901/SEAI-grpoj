import ezr
import step01
import step07

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (low ydist) and is small (low N_estimators).
    We use the acquire logic to explore the space, but we modify the ranking
    to favor both low ydist and low N_estimators.
    """
    # Create a table to handle column roles
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Identify the N_estimators column index
    n_est_idx = header.index("N_estimators")
    
    # Define a custom ranker that balances performance (ydist) and size (N_estimators)
    # We normalize N_estimators to 0..1 to balance it against ydist
    def combined_score(row):
        yd = ezr.ydist(tbl, row)
        # Normalize N_estimators: (val - min) / (max - min)
        # Since we don't have global min/max easily, we use the column's range
        # or just the raw value if we assume it's within a reasonable range.
        # A simple heuristic: lower N_estimators is better.
        norm_n = row[n_est_idx] / 200.0 
        return yd + (0.2 * norm_n) # Weight size at 20% of the performance score

    best_row_info = {"row": None, "score": 1e30}

    def tracked_label(i):
        full_row = label(i)
        score = combined_score(full_row)
        if score < best_row_info["score"]:
            best_row_info["score"] = score
            best_row_info["row"] = full_row
        return full_row

    # Use the acquire logic to find the best setup
    # We pass the tracked_label to ensure we stay within the 50-label budget
    # We need to map the acquire logic to our label function
    # Since acquire works on a TBL, we use the indices to label
    
    # We use the existing acquire logic from step07/ezr
    # We need to provide a way to label rows by index
    def oracle_wrapper(row):
        # Find index of row in original rows
        for i, r in enumerate(rows):
            if r == row: return tracked_label(i)
        return row

    ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Return the index of the best row found
    return rows.index(best_row_info["row"])

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Mask goals
    temp_tbl = ezr.Tbl([header] + rows)
    goal_indices = [c.at for c in temp_tbl.y]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i): return rows[i]
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete. The best setup (balancing performance and size) is at index {best_idx}.")
    print(f"Row details: {rows[best_idx]}")
    exit(0)
