import ezr
import step01

def spot(header, rows):
    """
    Identify rows that are 'outliers' in the input space.
    We use the distance of each row from the median of the dataset 
    as a measure of how 'unusual' or 'mistyped' a row is.
    """
    # Create a table to handle normalization of inputs
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the distance of each row from the central tendency (mids)
    # Rows that are far from the median in input space are suspicious.
    # We use xdist to compare rows against the median of the whole table.
    median_row = ezr.mids(tbl)
    
    # Calculate distance for each row
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, median_row)
        distances.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    distances.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in distances[:limit]]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially mistyped or anomalous records.")
    print("-" * 60)
    print(f"Found {len(suspicious_indices)} suspicious configurations.")
    print("These rows are the most distant from the dataset's central tendency:")
    print("-" * 60)
    print(f"{'Index':<10} | {'Distance from Median':<20}")
    print("-" * 60)
    
    # Re-calculate distances for display
    tbl = ezr.Tbl([header] + rows)
    median_row = ezr.mids(tbl)
    
    for idx in suspicious_indices:
        dist = ezr.xdist(tbl, rows[idx], median_row)
        print(f"{idx:<10} | {dist:.4f}")
        
    print("-" * 60)
    print("These records may warrant manual review for data entry errors.")
