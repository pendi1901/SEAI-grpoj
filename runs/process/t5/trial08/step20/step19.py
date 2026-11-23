import ezr
import random

def spot(header, rows):
    """
    Identify rows that are 'unlike anything we have run'.
    We define suspicious rows as those that are outliers in the input space
    (x-columns) relative to the rest of the data. We use the distance from
    the centroid of the input space as a measure of suspicion.
    """
    # Create a table to handle column roles
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space (x-columns)
    # The 'mids' function provides the median/mean for each column.
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # Higher distance = more suspicious (outlier/unseen)
    suspicious_scores = []
    for i, row in enumerate(rows):
        # xdist calculates the distance between a row and the centroid
        d = ezr.xdist(tbl, row, centroid)
        suspicious_scores.append((d, i))
    
    # Sort by distance descending (most suspicious/unseen first)
    suspicious_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the rows
    return [item[1] for item in suspicious_scores]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty or missing.")
        exit(1)
        
    # Get the suspicious indices
    suspicious_indices = spot(header, rows)
    
    # Print the top 5 most suspicious (unseen) setups
    print("Analysis: Identifying setups that are unlike anything we have run.")
    print("The following row indices represent the most unique/unseen configurations:")
    for idx in suspicious_indices[:5]:
        print(f" - Row index {idx}")
        
    print("\nThese configurations deviate significantly from our historical data.")
    print("Proceed with caution as these are outside our known operational experience.")
    
    exit(0)
