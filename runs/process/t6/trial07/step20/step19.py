import ezr
import step09

def spot(header, rows):
    """
    Identify rows that contain input values that are 'unlike anything we have run'.
    We define this as rows that have a high distance (xdist) to the nearest 
    neighbor in the training data. A high xdist indicates that the input 
    combination is rare or anomalous compared to the known distribution.
    """
    # Create a table to handle distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # For each row, calculate the distance to its nearest neighbor in the dataset.
    # A high distance to the nearest neighbor means the row is an outlier in the input space.
    anomalies = []
    for i, row in enumerate(rows):
        # Find the distance to the closest row (excluding itself)
        # We use xdist to compare input characteristics
        min_dist = 1e30
        for j, other in enumerate(rows):
            if i == j: continue
            d = ezr.xdist(tbl, row, other)
            if d < min_dist:
                min_dist = d
        anomalies.append((min_dist, i))
    
    # Sort by distance descending (most suspicious/unique first)
    anomalies.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[1] for item in anomalies[:10]]

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying setups that are unlike anything we have run.")
    print(f"Found {len(suspicious_indices)} most unique/suspicious rows:")
    print("-" * 50)
    print(f"{'Row Index':<12} | {'Uniqueness Score (xdist to nearest)'}")
    print("-" * 50)
    
    tbl = ezr.Tbl([header] + rows)
    
    for idx in suspicious_indices:
        row = rows[idx]
        # Re-calculate score for display
        min_dist = 1e30
        for j, other in enumerate(rows):
            if idx == j: continue
            d = ezr.xdist(tbl, row, other)
            if d < min_dist: min_dist = d
        print(f"{idx:<12} | {min_dist:.4f}")
        
    print("\nThese rows represent configurations that are significantly different from our historical data.")
    exit(0)
