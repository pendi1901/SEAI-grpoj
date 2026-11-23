import ezr
import random

def spot(header, rows):
    """
    Find rows that look wrong. We define 'wrong' as rows that are 
    outliers in the input space (x-columns) relative to the rest of the data.
    We use the distance to the nearest neighbor in the input space as a 
    measure of suspicion: rows that are very far from all other rows 
    are likely to contain typos or invalid entries.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # We focus on input columns (x-columns) to find data entry errors
    # as these are independent of the goal outcomes.
    # For each row, calculate the distance to its nearest neighbor.
    # A high distance to the nearest neighbor suggests an outlier.
    
    n = len(rows)
    if n < 2:
        return []
    
    # Calculate distances between all rows in the input space
    # To be efficient, we sample if the dataset is large, but here
    # we can compute distances for the provided rows.
    suspicion = []
    for i in range(n):
        min_dist = float('inf')
        for j in range(n):
            if i == j:
                continue
            d = ezr.xdist(tbl, rows[i], rows[j])
            if d < min_dist:
                min_dist = d
        suspicion.append((min_dist, i))
    
    # Sort by distance descending: the rows with the largest "nearest neighbor"
    # distance are the most isolated/suspicious.
    suspicion.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[1] for item in suspicion[:10]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print("The following rows are the most suspicious based on input space outliers:")
    for i, idx in enumerate(suspicious_indices[:5]):
        print(f"  {i+1}. Row index {idx} (Distance to nearest neighbor: high)")
    
    print("\nThese rows may contain typos or invalid values in input columns.")
    exit(0)
