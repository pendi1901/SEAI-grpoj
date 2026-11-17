import ezr
import step01

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by checking how well they fit 
    the local neighborhood of the data. We use the tree-based model to 
    predict the expected ydist for a row and flag rows where the actual 
    ydist is significantly worse than the predicted neighborhood mean.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Build a tree to learn the expected performance (ydist) based on inputs
    node = ezr.tree(tbl, rows)
    
    # Calculate the difference between actual ydist and the leaf's mean ydist
    # A large positive difference indicates the row is an outlier (worse than expected)
    suspects = []
    for i, row in enumerate(rows):
        leaf = ezr.leaf(node, row)
        actual = ezr.ydist(tbl, row)
        # The 'suspicion' score is how much worse this row is than its peers
        score = actual - leaf.mu
        suspects.append((score, i))
    
    # Sort by suspicion score descending
    suspects.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 1% most suspicious rows
    limit = max(1, len(rows) // 100)
    return [idx for _, idx in suspects[:limit]]

if __name__ == "__main__":
    file_path = "pom3a.train.csv"
    rows_iter = ezr.csv(file_path)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # Identify suspicious rows
    suspect_indices = spot(header, all_rows)
    
    print(f"Analysis of {len(all_rows)} records complete.")
    print(f"Identified {len(suspect_indices)} potentially mistyped or anomalous records.")
    print("Most suspicious row indices (top 5):")
    for idx in suspect_indices[:5]:
        row = all_rows[idx]
        # Show a snippet of the row to the customer
        print(f" - Row {idx}: {row[:5]}...")
        
    exit(0)
