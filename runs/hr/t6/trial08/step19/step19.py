import ezr
import step09

def spot(header, rows):
    """
    Identifies rows that are suspicious because they deviate significantly 
    from the established patterns of the dataset. We reuse the logic from 
    step09, which calculates the distance of each row from the centroid 
    of the input columns (xdist). Rows with the highest xdist are the 
    most suspicious.
    """
    # We use the logic from step09 to identify suspicious records.
    # step09.spot returns the indices of the top 10 most suspicious rows.
    return step09.spot(header, rows)

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Trustworthiness Analysis: Detecting Anomalous Hires")
    print("-" * 60)
    print("The following rows represent records that deviate significantly")
    print("from our historical employee patterns. Estimates for these")
    print("individuals may be unreliable due to their unique characteristics.")
    print("-" * 60)
    print(f"{'Rank':<6} | {'Row Index':<10} | {'Suspicion Score'}")
    
    # Re-calculate distances for display
    tbl = ezr.Tbl([header] + rows)
    centroid = ezr.mids(tbl)
    
    for rank, idx in enumerate(suspicious_indices, 1):
        score = ezr.xdist(tbl, rows[idx], centroid)
        print(f"{rank:<6} | {idx:<10} | {score:.2f}")
        
    print("-" * 60)
    print("Recommendation: Proceed with caution when using model predictions")
    print("for these specific records.")
