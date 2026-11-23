import ezr
import step09

def spot(header, rows):
    """
    Identify suspicious rows. A row is suspicious if its input values
    are outliers compared to the rest of the dataset. We use the 
    distance from the centroid of the input space (xdist) as a measure 
    of how 'unusual' a row is.
    
    This reuses the logic from step09.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    # Identify suspicious rows
    suspect_indices = spot(header, rows)
    
    print("Anomaly Detection Report:")
    print("The following configurations are highly unusual compared to our historical data.")
    print("These may represent new, untested, or potentially mistyped setups.")
    print(f"{'Rank':<10} | {'Row Index':<10}")
    print("-" * 25)
    
    # Print the top 5 most suspicious rows
    for rank, idx in enumerate(suspect_indices[:5]):
        print(f"{rank+1:<10} | {idx:<10}")
        
    exit(0)
