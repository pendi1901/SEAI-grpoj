import ezr
import step01

def flow(header, row, seen):
    """
    Decides whether to stop at the current row.
    We stop if the current row is in the top 5% of all potential rows,
    estimated by comparing it against the distribution of seen rows.
    """
    if not seen:
        return False
    
    # Create a table to use ezr's distance metrics
    # We use the seen rows to establish the context of what is "good"
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the ydist of the current row
    # A lower ydist is better (closer to ideal goals)
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate the ydist of all previously seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # We stop if the current row is better than 95% of what we have seen so far
    # (i.e., it is in the top 5% of the current distribution)
    threshold = sorted(seen_ydists)[int(len(seen_ydists) * 0.05)]
    
    return current_ydist <= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    seen = []
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopped at row {i+1} (1-based index).")
            print(f"Row values: {row}")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("No row met the criteria; processed all rows.")
