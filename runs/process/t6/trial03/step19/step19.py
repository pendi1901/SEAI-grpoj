import ezr
import step09

def spot(header, rows):
    """
    Identify rows that are 'outliers' in the input space.
    We use the distance from the centroid of the data as a measure of suspicion.
    Rows that are far from the center of the input space are most suspicious.
    This reuses the logic from step09 to detect setups the team has never seen.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying setups that are unlike anything we have run before.")
    print(f"Found {len(suspicious_indices)} rows that are highly suspicious (outliers).")
    print("These represent configurations that deviate significantly from our historical data.")
    print("Top 5 most suspicious row indices:")
    print(suspicious_indices[:5])
    
    # Exit with status 0
    exit(0)
