import ezr
import step09

def spot(header, rows):
    """
    Identify rows that do not fit the distribution of the data.
    We use the distance from the centroid of the input (X) columns
    as a measure of 'suspicion'. Rows that are far from the 
    center of the input space are considered outliers.
    
    This reuses the logic from step09.py.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Get suspicious indices
    suspicious_indices = spot(header, rows)
    
    print("Anomaly Detection: Identifying setups unlike anything seen before.")
    print(f"Found {len(suspicious_indices)} suspicious rows.")
    print("The following rows are the most 'unusual' based on input distributions:")
    
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f"- Row {idx} is highly suspicious (outlier in input space).")
        
    exit(0)
