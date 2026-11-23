import ezr
import random

def spot(header, rows):
    """
    Returns a list of row indices that are most suspicious.
    A row is suspicious if it is an outlier in the input space (xdist)
    relative to the central tendency of the dataset.
    """
    # Create a table to handle column definitions and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid (mids) of the dataset
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # We use xdist because we are looking for suspicious input values
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        distances.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    distances.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the rows, most suspicious first
    return [idx for d, idx in distances]

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous or 'untrustworthy' data entries.")
    print("The following rows are the most statistically distant from the dataset's central tendency,")
    print("meaning our model's estimates for these types of employees may be unreliable:")
    
    for rank, idx in enumerate(suspicious_indices[:5]):
        print(f"  Rank {rank+1}: Row {idx} (Distance from norm: high)")
        
    print("\nNote: These rows contain input values that deviate significantly from the rest of the data.")
    exit(0)
