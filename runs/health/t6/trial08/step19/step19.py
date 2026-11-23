import ezr
import step09

def spot(header, rows):
    """
    Identify suspicious rows (outliers) that contain input values 
    far from the observed distribution.
    
    We reuse the logic from step09, which calculates the distance 
    of each row from the median input values (xdist). Rows with 
    high xdist are those with input values we have rarely or 
    never seen in the context of the rest of the data.
    """
    # Use the logic from step09 to identify the most suspicious rows
    return step09.spot(header, rows)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete on {len(rows)} records.")
    print(f"Identified {len(suspicious_indices)} rows with input values that are highly unusual.")
    print("These rows contain settings far outside the typical range observed in the dataset.")
    print("Top 5 most suspicious indices (0-based):", suspicious_indices[:5])
    
    exit(0)
