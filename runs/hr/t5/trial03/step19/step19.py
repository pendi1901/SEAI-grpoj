import ezr
import random

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' by finding 
    outliers in the input space. A row is suspicious if its input values 
    are far from the expected distribution of the rest of the data 
    (using xdist).
    """
    # Create a table to handle the data and column normalization
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the entire dataset.
    # The library's mids() provides the central tendency for all columns.
    # This represents the "typical" employee.
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid.
    # Rows that are very far from the centroid are likely outliers 
    # or "unlike anyone we have employed".
    scores = []
    for i, row in enumerate(rows):
        # xdist measures distance across input columns (excluding goals).
        d = ezr.xdist(tbl, row, centroid)
        scores.append((d, i))
    
    # Sort by distance descending (most suspicious/unlike others first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the rows that are most suspicious.
    # We return the top 10 as a reasonable set of outliers.
    return [idx for d, idx in scores[:10]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("--- Anomaly Detection: Employees Unlike Current Staff ---")
    print(f"Identified {len(suspicious_indices)} records that are statistically distinct from our current workforce.")
    print("These records represent candidates or employees whose profiles are 'unlike anyone we have employed'.")
    print("Our estimates for these individuals may be less reliable due to their unique profiles.")
    print("\nMost suspicious row indices (most to least):")
    print(suspicious_indices)
    
    # Show a brief summary of the most suspicious row
    top_idx = suspicious_indices[0]
    row = rows[top_idx]
    print(f"\nExample of an 'unlike' profile (Row Index {top_idx}):")
    # Show a few key input columns
    for i in range(min(6, len(header))):
        print(f"  {header[i]}: {row[i]}")
    
    exit(0)
