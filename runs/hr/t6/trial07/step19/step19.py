import ezr
import step09

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed'.
    We use the distance from the global centroid (mids) in the input space.
    Rows that are extreme outliers (high xdist) are those that the model
    has not seen before and thus cannot reliably estimate.
    """
    # Create a table to handle normalization and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate the centroid of the data
    centroid = ezr.mids(tbl)
    
    # Calculate xdist for every row
    # xdist measures how far a row's inputs are from the average inputs
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, row, centroid)
        distances.append((d, i))
    
    # Sort by distance descending (most suspicious/unlike others = furthest from typical)
    distances.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the rows that are most 'unlike' our historical data
    return [idx for d, idx in distances]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify rows that are unlike our historical data
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying hires that are unlike anyone we have employed.")
    print("The following rows represent the most 'unusual' profiles (outliers in input space).")
    print("Estimates for these individuals are the least trustworthy:")
    
    # Print the top 5 most suspicious
    tbl = ezr.Tbl([header] + rows)
    centroid = ezr.mids(tbl)
    for idx in suspicious_indices[:5]:
        dist = ezr.xdist(tbl, rows[idx], centroid)
        print(f"- Row {idx} (Distance from typical profile: {dist:.2f})")
    
    print("\nThese individuals deviate significantly from our historical employee base, "
          "making our predictive models less reliable for them.")
