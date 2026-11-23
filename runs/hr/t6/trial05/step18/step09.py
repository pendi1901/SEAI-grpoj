import ezr
import random

def spot(header, rows):
    """
    Finds rows that look 'wrong' by identifying outliers.
    A row is suspicious if it is very far from the 'mids' (centroids)
    of the dataset, as these represent anomalies in the input space.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the distance of each row from the global centroid (mids)
    # Rows with high xdist are outliers in the input space.
    centroid = ezr.mids(tbl)
    
    # Calculate xdist for every row
    scored = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        scored.append((d, i))
    
    # Sort by distance descending (most suspicious/outlier first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[1] for item in scored[:10]]

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print("The following rows are the most suspicious (outliers in input space):")
    for i, idx in enumerate(suspicious_indices[:5]):
        print(f"{i+1}. Row index {idx} (Distance from norm: high)")
    
    print("\nThese rows contain input values that deviate significantly from the rest of the dataset.")
    exit(0)
