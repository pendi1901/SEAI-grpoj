import ezr
import random

def spot(header, rows):
    """
    Identifies suspicious rows by finding those that are 'outliers' 
    relative to their local neighborhood in the data space.
    
    We use the tree structure to group similar rows. A row is suspicious 
    if its ydist (performance) is significantly worse than the mean 
    ydist of its leaf node, suggesting it might be an anomaly or 
    data entry error.
    """
    # Create a table to calculate ydist and build the tree
    tbl = ezr.Tbl([header] + rows)
    
    # Build a tree to cluster similar rows
    root = ezr.tree(tbl, rows)
    
    # Calculate the deviation of each row from its leaf's mean performance
    # Suspiciousness = (row_ydist - leaf_mean_ydist)
    # Higher deviation means the row is an outlier in its own cluster
    suspects = []
    for i, row in enumerate(rows):
        leaf = ezr.leaf(root, row)
        row_ydist = ezr.ydist(tbl, row)
        # We look for rows that perform much worse than their peers
        deviation = row_ydist - leaf.mu
        suspects.append((deviation, i))
    
    # Sort by deviation descending (most suspicious first)
    suspects.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [i for dev, i in suspects[:10]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print("The following rows are most suspicious based on their deviation from local performance norms:")
    
    for rank, idx in enumerate(suspicious_indices[:5]):
        print(f"  Rank {rank+1}: Row index {idx}")
        
    print("\nMethodology: Rows were clustered using a decision tree. Rows with performance metrics")
    print("significantly worse than their cluster average were flagged as potential data entry errors.")
    
    exit(0)
