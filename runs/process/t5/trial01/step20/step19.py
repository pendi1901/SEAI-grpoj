import ezr
import random

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by checking if their input values
    are outliers compared to the rest of the population.
    
    We use the distance of each row's input values (xdist) from the 
    median of all rows. Rows that are significantly far from the median 
    in the input space are flagged as potential outliers.
    """
    # Create a table to handle column logic
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the median of all rows in the input space
    # ezr.mids(tbl) returns the centroid of the data
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # We use xdist to measure distance in the input space
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        distances.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    distances.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the most suspicious rows
    return [item[1] for item in distances]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Anomaly Detection Report:")
    print("The following rows contain input values that deviate significantly from the norm.")
    print("These configurations are unlike anything we have seen before:")
    
    # Print the top 5 most suspicious
    for i, idx in enumerate(suspicious_indices[:5], 1):
        print(f"{i}. Row index {idx} (Distance: {ezr.xdist(ezr.Tbl([header]+rows), rows[idx], ezr.mids(ezr.Tbl([header]+rows))):.4f})")
        
    print("\nThese rows are the most suspicious and should be reviewed for data entry errors.")
    exit(0)
