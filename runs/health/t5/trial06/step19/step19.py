import ezr
import random

def spot(header, rows):
    """
    Identify rows containing input values that are 'suspicious' or 'unseen'.
    A row is suspicious if its input values are far from the distribution 
    observed in the rest of the data (outliers).
    """
    # Create a table to manage column roles and distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid (mids) of the data to define 'normal'
    mids = ezr.mids(tbl)
    
    suspicion_scores = []
    
    for i, row in enumerate(rows):
        # Calculate 'strangeness' of inputs: 
        # How far is this row's input from the global centroid?
        # xdist measures distance over the x-columns.
        strangeness = ezr.xdist(tbl, row, mids)
        
        # A high strangeness score indicates the row contains values 
        # that are far from the typical values seen in the dataset.
        suspicion_scores.append((strangeness, i))
    
    # Sort by strangeness descending (most suspicious/unseen first)
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion_scores]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying setups that are far outside the norm.")
    print(f"Found {len(suspicious_indices)} rows. Top 5 most suspicious indices:")
    for idx in suspicious_indices[:5]:
        print(f"Row {idx}: {rows[idx]}")
        
    print("\nThese rows were flagged because their input configurations are "
          "statistically distant from the rest of the observed data.")
    
    exit(0)
