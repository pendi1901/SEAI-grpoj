import ezr
import step01

def remember(header, rows):
    """
    Identify the top 5% of rows based on multi-objective optimization.
    A row is better if its goals (ending in + or -) are closer to their ideal.
    """
    # Create a table object using the provided rows
    # The ezr.Tbl function expects the header as the first row of the input
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for every row. ydist measures how far a row is from
    # the ideal goal values (0 for -, 1 for +).
    # We want to minimize ydist.
    scored = []
    for i, row in enumerate(rows):
        d = ezr.ydist(tbl, row)
        scored.append((d, i))
    
    # Sort by distance (ascending)
    scored.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5%
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load the data
    file_path = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(file_path))
    header = all_data[0]
    rows = all_data[1:]
    
    # Get the best indices
    best_indices = remember(header, rows)
    
    # Print results
    print("Top-performing configurations found:")
    tbl = ezr.Tbl([header] + rows)
    for idx in best_indices:
        score = ezr.ydist(tbl, rows[idx])
        print(f"Index {idx:3}: ydist = {score:.4f}")
    
    print(f"\nAnalysis complete. Found {len(best_indices)} top-performing configurations.")
