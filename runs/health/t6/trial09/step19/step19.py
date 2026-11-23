import ezr
import step09

def spot(header, rows):
    """
    Identify rows that contain input values that are 'suspicious' or 
    'never seen' by comparing them to the distribution of the training data.
    We reuse the logic from step09, which identifies outliers in the 
    input (X) space using distance from the centroid.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete on {len(rows)} records.")
    if suspicious_indices:
        print(f"Identified {len(suspicious_indices)} rows with settings that are "
              "statistically distant from the known data (potential outliers).")
        print("Top 5 most suspicious row indices:", suspicious_indices[:5])
    else:
        print("No suspicious rows identified.")
        
    exit(0)
