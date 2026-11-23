import ezr
import step09

def spot(header, rows):
    """
    Identify rows that contain input values far outside the observed range
    or distribution of the training data. We use the xdist metric to find
    rows that are outliers in the input space.
    """
    # We reuse the logic from step09 which calculates xdist from the centroid
    # of the input space. Rows with high xdist are those with values 
    # significantly different from the average, which covers the colleague's
    # suggestion of settings "far outside anything we have tried".
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    suspicious_indices = spot(header, rows)
    
    print("--- Analysis: Outlier Detection ---")
    print("The following rows contain input settings that are far outside")
    print("the range of our historical data:")
    
    if not suspicious_indices:
        print("No suspicious rows found.")
    else:
        for idx in suspicious_indices[:5]:
            print(f"- Row {idx} is highly suspicious (xdist outlier).")
            
    print("\nThese configurations should be treated with caution as they")
    print("represent settings we have never seen before.")
    exit(0)
