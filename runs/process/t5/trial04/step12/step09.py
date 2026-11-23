import ezr
import random

def spot(header, rows):
    """
    Identify rows that do not fit the distribution of the data.
    We use the distance of each row from the 'middle' (centroid) of the 
    dataset as a measure of suspicion. Rows that are outliers in the 
    input space (X columns) are flagged as suspicious.
    """
    # Create a table to handle column statistics
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid (mids) of the dataset
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # We use xdist because we are looking for input anomalies
    suspicion_scores = []
    for i, row in enumerate(rows):
        # xdist calculates the distance between a row and the centroid
        score = ezr.xdist(tbl, row, centroid)
        suspicion_scores.append((score, i))
    
    # Sort by score descending (most suspicious first)
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[1] for item in suspicion_scores[:10]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty.")
        exit(1)
        
    # Get the most suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Anomaly Detection Report")
    print("-" * 60)
    print("The following rows are the most suspicious (outliers in input space):")
    print(f"{'Row Index':<15} | {'Suspicion Score'}")
    print("-" * 60)
    
    # Re-calculate scores for display
    tbl = ezr.Tbl([header] + rows)
    centroid = ezr.mids(tbl)
    for idx in suspicious_indices:
        score = ezr.xdist(tbl, rows[idx], centroid)
        print(f"{idx:<15} | {score:.4f}")
        
    print("-" * 60)
    print("These rows deviate significantly from the central tendencies of the")
    print("dataset and may contain mistyped or erroneous input values.")
    
    exit(0)
