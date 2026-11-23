import ezr
import random

def flow(header, row, seen):
    """
    Detects if a team (represented by the current row) looks 'abnormal' 
    compared to the history of teams seen so far.
    
    We define 'abnormal' as being statistically distant from the 
    distribution of previously seen rows in the input space.
    """
    # We need a baseline to define 'normal'. 
    # If we have too few rows, we cannot reliably detect anomalies.
    if len(seen) < 30:
        return False
    
    # Create a table from the history to calculate the central tendency
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the centroid (mids) of the history
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of the current row from the centroid
    # We use xdist because we are looking for input-space anomalies
    current_dist = ezr.xdist(tbl, row, centroid)
    
    # Calculate distances for all seen rows to establish a threshold
    seen_dists = [ezr.xdist(tbl, r, centroid) for r in seen]
    
    # Use a simple statistical threshold: 
    # If the current row is more than 2 standard deviations away from the 
    # mean distance of the history, it is considered 'abnormal'.
    mu = sum(seen_dists) / len(seen_dists)
    sd = (sum((d - mu)**2 for d in seen_dists) / len(seen_dists))**0.5
    
    # Flag if the row is an outlier (e.g., > 2 standard deviations)
    return current_dist > (mu + 2 * sd)

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    anomalies = 0
    
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print("Analysis: Detecting abnormal team structures in incoming data.")
    print(f"Total records processed: {len(rows)}")
    print(f"Number of records flagged as 'abnormal' (statistically distant): {anomalies}")
    print("Logic: A record is flagged if its input features deviate significantly "
          "from the historical mean ( > 2 standard deviations).")
    
    exit(0)
