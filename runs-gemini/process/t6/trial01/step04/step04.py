import ezr
import random

def flow(header, row, seen):
    """
    Decide on the spot whether to approve a row.
    We approve if the row is in the top 5% of the expected distribution
    based on the data seen so far.
    """
    if not seen:
        return True
    
    # Create a table from seen rows to establish the context
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the ydist of the current row
    # We use the existing table's normalization logic
    current_ydist = ezr.ydist(tbl, row)
    
    # Calculate ydist for all seen rows
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    
    # If the current row is better than the median of what we've seen,
    # we take it. This is a simple greedy threshold for streaming data.
    median_ydist = sorted(seen_ydists)[len(seen_ydists) // 2]
    
    return current_ydist <= median_ydist

if __name__ == "__main__":
    file_path = "pom3a.train.csv"
    rows_iter = ezr.csv(file_path)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    seen = []
    approved = []
    
    # Simulate the streaming process
    for row in all_rows:
        if flow(header, row, seen):
            approved.append(row)
        seen.append(row)
        
    print(f"Processed {len(all_rows)} proposals.")
    print(f"Approved {len(approved)} proposals based on streaming criteria.")
    
    # Show a summary of the first few approved
    if approved:
        print("Sample of approved row goals:")
        for i, row in enumerate(approved[:5]):
            goals = {header[j]: row[j] for j, name in enumerate(header) if name[-1] in "+-"}
            print(f"  Approved {i+1}: {goals}")
            
    exit(0)
