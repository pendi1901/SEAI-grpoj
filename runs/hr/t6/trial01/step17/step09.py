import ezr
import random

def spot(header, rows):
    """
    Find rows that look wrong. We define 'wrong' as rows that are 
    outliers in the input space (x-columns) relative to the rest of the data.
    We use the distance to the nearest neighbor in the x-space to identify
    rows that are 'far' from the rest of the population.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the distance of each row to the centroid of the data
    # Rows that are very far from the centroid are suspicious.
    # We use xdist to measure distance in the input space.
    centroid = ezr.mids(tbl)
    
    # Calculate distance for each row
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        distances.append((i, d))
    
    # Sort by distance descending (most suspicious first)
    distances.sort(key=lambda x: x[1], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[0] for item in distances[:10]]

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print("The following rows are the most suspicious (outliers in input space):")
    
    for idx in suspicious_indices[:5]:
        row = rows[idx]
        # Show a few key columns to help the user verify
        age_idx = header.index('Age')
        role_idx = header.index('jobRole')
        print(f" - Row {idx}: Age {row[age_idx]}, Role {row[role_idx]}")
        
    print("\nLogic: Rows identified as having the largest distance from the "
          "population centroid in the input feature space.")
