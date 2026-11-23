import ezr
import random

def spot(header, rows):
    """
    Identifies rows that are 'unlike' the rest of the population.
    We use the distance of each row from the 'mids' (centroids) of the 
    entire dataset. Rows that are significantly distant from the 
    typical values in their respective x-columns are flagged as suspicious.
    This effectively identifies rows that cannot be trusted because 
    they fall outside the model's training distribution.
    """
    # Create a table to leverage ezr's column statistics
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the 'mids' (centroids) for all columns
    centroids = ezr.mids(tbl)
    
    # Calculate a 'suspicion score' for each row.
    # A row is suspicious if its x-columns are far from the global centroid.
    # We use xdist to measure this distance.
    scores = []
    for i, row in enumerate(rows):
        # Calculate distance from the centroid
        d = ezr.xdist(tbl, row, centroids)
        scores.append((d, i))
    
    # Sort by distance descending (most suspicious/unlike first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the most suspicious rows
    return [item[1] for item in scores]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying unreliable employee records.")
    print("We flag records that are statistical outliers compared to the historical norm.")
    print("Estimates for these rows cannot be trusted as they represent profiles unlike any we have employed.")
    print("\nTop 5 most suspicious row indices:")
    for i in suspicious_indices[:5]:
        print(f"- Row index: {i}")
    
    print("\nThese rows should be manually reviewed before making any hiring or retention decisions.")
