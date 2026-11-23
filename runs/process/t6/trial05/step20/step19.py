import ezr
import step09

def spot(header, rows):
    """
    Identify rows that are 'unlike anything we have run'.
    We reuse the logic from step09 which identifies outliers in the 
    input space by calculating the distance to the centroid of the data.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    # Print results
    print("Analysis: Identifying setups that are unlike anything seen in historical data.")
    print(f"Found {len(suspicious_indices)} setups that appear highly unusual.")
    
    if suspicious_indices:
        print(f"The most suspicious setup is at index {suspicious_indices[0]}.")
        print("This setup is an outlier in the input space and may be a data entry error.")
    else:
        print("No highly unusual setups were detected.")
        
    exit(0)
