import ezr
import random

def spot(header, rows):
    """
    Identify suspicious rows. A row is suspicious if its input values are 
    outliers compared to the rest of the data, or if it has an unusually 
    high ydist (poor performance) despite having 'normal' input values.
    
    We use the distance from the median of each column as a measure of 
    'strangeness' for inputs.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the median for each input column to define 'normal'
    # We use the cached mids from the table
    mids = ezr.mids(tbl)
    
    suspicion_scores = []
    
    for i, row in enumerate(rows):
        # Calculate 'strangeness' of inputs: 
        # How far is this row's input from the global median?
        # We use xdist to measure distance from the centroid of the data.
        strangeness = ezr.xdist(tbl, row, mids)
        
        # Calculate performance: ydist
        # A row that is 'normal' (low strangeness) but has very poor 
        # performance (high ydist) is highly suspicious.
        performance = ezr.ydist(tbl, row)
        
        # Score: High strangeness or high ydist for a 'normal' row
        # We weight performance heavily if the row is otherwise 'normal'.
        score = strangeness + (performance * 5.0)
        suspicion_scores.append((score, i))
    
    # Sort by score descending (most suspicious first)
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
    
    print("Analysis: Identifying potentially failed or erroneous runs.")
    print(f"Found {len(suspicious_indices)} rows. Top 5 most suspicious indices:")
    for idx in suspicious_indices[:5]:
        print(f"Row {idx}: {rows[idx]}")
        
    print("\nThese rows were flagged based on high input strangeness or "
          "poor performance relative to their input configuration.")
    
    exit(0)
