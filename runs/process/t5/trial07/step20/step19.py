import ezr
import random

def spot(header, rows):
    """
    Identify rows that are 'suspicious' by checking if they are outliers
    in the input space. We use the distance to the nearest neighbor 
    in the input space (xdist) as a metric for suspicion.
    Rows that are very far from all other rows are likely anomalous.
    """
    # Create a table to handle normalization and distance calculations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the distance of each row to its nearest neighbor in the input space.
    # We use a sample to keep performance reasonable for larger datasets.
    # For each row, we find the distance to the closest other row.
    suspicion_scores = []
    for i, r1 in enumerate(rows):
        min_dist = 1e30
        # Compare against a subset of rows to speed up calculation
        # if the dataset is large, but here we check against all.
        for j, r2 in enumerate(rows):
            if i == j:
                continue
            d = ezr.xdist(tbl, r1, r2)
            if d < min_dist:
                min_dist = d
        suspicion_scores.append((min_dist, i))
    
    # Sort by distance (descending: furthest from neighbors is most suspicious)
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the most suspicious rows
    return [item[1] for item in suspicion_scores]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    # Print the top 5 most suspicious rows
    print("Analysis: Identifying potentially anomalous or novel project configurations.")
    print("The following rows are the most suspicious based on their distance from other data points:")
    print(f"{'Rank':<6} | {'Row Index':<10} | {'Suspicion Score'}")
    print("-" * 40)
    
    # We re-calculate the distance for display purposes
    tbl = ezr.Tbl([header] + rows)
    for rank, idx in enumerate(suspicious_indices[:5], 1):
        # Find distance to nearest neighbor again for the score
        r1 = rows[idx]
        min_dist = 1e30
        for j, r2 in enumerate(rows):
            if idx == j: continue
            d = ezr.xdist(tbl, r1, r2)
            if d < min_dist: min_dist = d
        print(f"{rank:<6} | {idx:<10} | {min_dist:.4f}")
        
    print("\nThese records deviate significantly from the patterns found in the rest of the dataset.")
    print("If these are new proposals, they represent configurations we have never seen before.")
    exit(0)
