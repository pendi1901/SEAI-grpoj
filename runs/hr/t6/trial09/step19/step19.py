import ezr
import step09

def spot(header, rows):
    """
    Identifies rows that are suspicious because they are outliers in the input space.
    We reuse the logic from step09, which calculates the x-distance to the 
    nearest neighbor. Rows with the largest distance to their nearest neighbor 
    are the most suspicious (i.e., they are unlike anyone else we have employed).
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying records that are unlike anyone we have employed.")
    print("Method: Flagging rows that are statistical outliers in the input space.")
    print(f"The most suspicious row index is: {suspicious_indices[0]}")
    print(f"Top 5 most suspicious row indices: {suspicious_indices[:5]}")
    
    print("\nNote: These rows have the largest 'x-distance' to their nearest neighbors.")
    print("When a new hire's profile matches these indices, our estimates for them")
    print("cannot be trusted as they fall outside our historical experience.")
    
    exit(0)
