import ezr
import step01

def spot(header, rows):
    """
    Finds rows that look 'wrong' by identifying outliers.
    We define 'wrong' as rows that are significantly distant from the 
    centroid of the data in the input space (x-columns).
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the input space
    mids = ezr.mids(tbl)
    
    # Calculate xdist for every row from the centroid
    # Rows with high xdist are outliers (potentially entered wrongly)
    scored = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, mids)
        scored.append((d, i))
    
    # Sort by distance descending (most suspicious first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[1] for item in scored[:10]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print("The following rows are the most suspicious (outliers in input space):")
    for idx in suspicious_indices[:5]:
        print(f" - Row index {idx} (Distance from centroid: {ezr.xdist(ezr.Tbl([header]+rows), rows[idx], ezr.mids(ezr.Tbl([header]+rows))):.2f})")
    
    print("\nLogic: Rows with input values that deviate significantly from the "
          "global average (centroid) are flagged as potential data entry errors.")
