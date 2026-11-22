import ezr
import random

def spot(header, rows):
    """
    Identifies rows that are 'outliers' in the input space.
    We use the distance to the centroid of the input columns (x)
    as a measure of how 'unusual' a row is. Rows that are far from
    the centroid are considered suspicious.
    """
    # Create a table to handle column normalization and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the entire dataset.
    # The centroid represents the 'typical' record.
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid.
    # Rows with high distance are statistically unusual.
    scores = []
    for i, row in enumerate(rows):
        # xdist calculates the distance based on input columns (x).
        # This is the standard way to detect anomalies in the input space.
        d = ezr.xdist(tbl, row, centroid)
        scores.append((d, i))
    
    # Sort by distance descending (most unusual first).
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the rows, most suspicious first.
    return [item[1] for item in scores]

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Data Quality Analysis: Identifying potentially unreliable records.")
    print("The following row indices contain input values that deviate significantly")
    print("from the rest of the dataset (most suspicious first):")
    # Print the top 10 most suspicious indices
    print(suspicious_indices[:10])
    
    print("\nWhen a new hire's data is significantly distant from these established")
    print("patterns, our model's estimates for them cannot be trusted.")
    
    # Example: Print the most suspicious row
    if suspicious_indices:
        idx = suspicious_indices[0]
        print(f"\nExample of the most suspicious record (Index {idx}):")
        print(rows[idx])
