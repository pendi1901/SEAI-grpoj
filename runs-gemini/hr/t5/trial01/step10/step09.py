import ezr

def spot(header, rows):
    """
    Identifies rows that look 'wrong' (outliers).
    We define a row as suspicious if its input values are highly 
    inconsistent with the rest of the data, measured by the 
    distance of the row to the centroid of its local neighborhood.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the distance of each row to the global centroid (mids)
    # Rows that are very far from the 'average' behavior are suspicious.
    # We use xdist to measure distance in the input space.
    centroid = ezr.mids(tbl)
    
    # Calculate xdist for every row
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        distances.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    distances.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [idx for _, idx in distances[:10]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous or outlier records.")
    print("The following rows contain input values that are highly unusual")
    print("compared to the rest of the dataset, suggesting potential entry errors:")
    
    for i, idx in enumerate(suspicious_indices):
        print(f" {i+1}. Row {idx} (most suspicious)")
        
    print("\nThese records should be reviewed for data entry accuracy.")
