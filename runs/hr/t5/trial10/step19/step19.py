import ezr
import random

def spot(header, rows):
    """
    Identifies rows that are 'unlike' the existing population.
    We use the distance from the centroid of the input (x) columns.
    Rows with high xdist are outliers and their estimates cannot be trusted.
    """
    # Create a table to handle column definitions and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Get the centroid of the existing data
    centroid = ezr.mids(tbl)
    
    # Calculate suspicion score for each row:
    # The distance from the centroid of the input (x) columns.
    # A row that is far from the centroid is 'unlike' our existing data.
    scores = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        scores.append((d, i))
    
    # Sort by distance descending (most suspicious/unlike first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the rows, most suspicious first
    return [idx for d, idx in scores]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Trust Analysis: Identifying employees unlike our current workforce.")
    print("Estimates for these records are less reliable due to their unique characteristics.")
    
    print("\nTop 5 most 'unlike' records (most suspicious):")
    for idx in suspicious_indices[:5]:
        row = rows[idx]
        # Print a few key columns to help the user verify
        print(f"Row {idx}: Age={row[0]}, JobRole={row[15]}, MonthlyIncome={row[18]}")
        
    print("\nRecommendation: Exercise caution when using model predictions for these specific records.")
    exit(0)
