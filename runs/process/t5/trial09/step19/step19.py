import ezr
import random

def spot(header, rows):
    """
    Identify rows that contain suspicious input values.
    We use the distance of each row from the 'middle' of the population
    as a proxy for how 'unusual' or 'mistyped' a row is.
    Rows with high xdist from the median row are flagged as suspicious.
    """
    # Create a table to handle column statistics
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the median row (mids)
    median_row = ezr.mids(tbl)
    
    # Calculate xdist for every row from the median
    # Higher xdist means the row is more of an outlier
    suspicious = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, median_row)
        suspicious.append((d, i))
    
    # Sort by distance (descending, as higher distance is more suspicious)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the rows, most suspicious first
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    # Print the top 5 most suspicious rows for the customer
    print("Outlier Detection: Identifying Unseen/Suspicious Setups")
    print("-" * 60)
    print("The following rows contain input configurations that deviate")
    print("significantly from our historical data, suggesting they are")
    print("unseen or potentially erroneous setups.")
    print("-" * 60)
    print(f"{'Row Index':<12} | {'Suspicion Score (xdist)'}")
    print("-" * 60)
    
    tbl = ezr.Tbl([header] + rows)
    median_row = ezr.mids(tbl)
    
    for idx in suspicious_indices[:5]:
        d = ezr.xdist(tbl, rows[idx], median_row)
        print(f"{idx:<12} | {d:.4f}")
        
    print("-" * 60)
    print("These setups are the most 'unlike anything we have run'.")
    exit(0)
