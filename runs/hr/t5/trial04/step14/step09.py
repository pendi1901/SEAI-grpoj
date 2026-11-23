import ezr
import random

def spot(header, rows):
    """
    Identifies rows that look 'wrong' by finding outliers in the input space.
    We use the distance to the centroid of the data (xdist) to find rows
    that are significantly different from the rest of the population.
    """
    # Create a table to handle column definitions and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid (mids) of the input columns
    # We use the cached mids from the table
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of each row from the centroid
    # A high xdist indicates that the row is an outlier in the input space
    scored = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        scored.append((d, i))
    
    # Sort by distance descending to find the most suspicious (outlier) rows
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[1] for item in scored[:10]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis of {len(rows)} employee records.")
    print("Identifying records that appear to be data entry errors (outliers):")
    
    for rank, idx in enumerate(suspicious_indices):
        row = rows[idx]
        # Print a few key fields to help the user verify the suspicion
        # Age (0), MonthlyIncome (18), TotalWorkingYears (28)
        print(f"{rank+1}. Row {idx}: Age={row[0]}, Income={row[18]}, YearsWorked={row[28]}")
        
    print("\nThese rows are the most statistically distant from the average employee record.")
    print("Manual review of these specific entries is recommended.")
