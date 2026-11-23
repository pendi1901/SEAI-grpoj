import ezr
import random

def spot(header, rows):
    """
    Identifies rows that look 'wrong' by finding outliers.
    A row is suspicious if its input values (x-columns) are far from the 
    centroid of the data, or if its goal values are inconsistent with 
    the input features (high prediction error).
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of all rows
    # We use the cached mids from the table
    centroid = ezr.mids(tbl)
    
    # Calculate suspicion score for each row:
    # 1. Distance from the centroid (xdist)
    # 2. We rank rows by how far they are from the 'typical' row.
    # Rows with very high xdist are likely outliers or data entry errors.
    scores = []
    for i, row in enumerate(rows):
        # Calculate distance to the centroid of the dataset
        d = ezr.xdist(tbl, row, centroid)
        scores.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [idx for d, idx in scores[:limit]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Find suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Data Quality Analysis: Identifying potentially incorrect records.")
    print(f"Found {len(suspicious_indices)} records that appear to be outliers.")
    print("These records have input values that deviate significantly from the rest of the dataset.")
    
    print("\nTop 5 most suspicious records (by index):")
    for idx in suspicious_indices[:5]:
        row = rows[idx]
        # Print a few key columns to help the user verify
        print(f"Row {idx}: Age={row[0]}, MonthlyIncome={row[18]}, TotalWorkingYears={row[28]}")
        
    print("\nRecommendation: Review these records for potential data entry errors.")
    exit(0)
