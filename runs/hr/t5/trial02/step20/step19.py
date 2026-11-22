import ezr
import random

def spot(header, rows):
    """
    Identifies rows that are 'unlike' the rest of the data.
    We use the tree structure to group similar rows. A row is suspicious 
    if its input characteristics (xdist) are significantly different 
    from the rest of the data in its cluster, or if it falls into a 
    very sparse region of the tree, indicating it is 'unlike' anyone 
    we have employed.
    """
    # Create a table to handle column definitions and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Build a tree to cluster similar rows
    root = ezr.tree(tbl, rows)
    
    # Suspiciousness is defined by how 'far' a row is from the centroid 
    # of its leaf node. A row that is an outlier in its own cluster 
    # is likely 'unlike' our typical employees.
    suspects = []
    for i, row in enumerate(rows):
        leaf = ezr.leaf(root, row)
        
        # Calculate distance from the row to the 'middle' of its leaf
        # We use xdist to compare input columns
        # We use the leaf's rows to calculate the centroid (mids)
        leaf_tbl = ezr.clone(tbl, leaf.rows)
        centroid = ezr.mids(leaf_tbl)
        
        deviation = ezr.xdist(tbl, row, centroid)
        
        # We also penalize rows that end up in very small leaves
        # (sparse regions of the data space)
        size_penalty = 1.0 / (len(leaf.rows) + 1)
        
        score = deviation + size_penalty
        suspects.append((score, i))
    
    # Sort by score descending (most suspicious/unlike first)
    suspects.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [i for score, i in suspects[:10]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying employees who are 'unlike' our typical staff.")
    print("The following rows are most suspicious because they represent unique")
    print("or outlier combinations of input characteristics:")
    
    for rank, idx in enumerate(suspicious_indices[:5]):
        print(f"  Rank {rank+1}: Row index {idx}")
        
    print("\nMethodology: Rows were clustered using a decision tree. Rows that")
    print("deviate significantly from their cluster's centroid or reside in")
    print("sparse regions of the data space are flagged as 'untrusted' estimates.")
    
    exit(0)
