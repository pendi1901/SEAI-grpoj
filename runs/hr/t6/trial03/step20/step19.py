import ezr
import step09

def spot(header, rows):
    """
    Identifies rows that are suspicious because they contain input values 
    that deviate significantly from the population average.
    Uses the logic from step09 to identify outliers in x-space.
    """
    # We use the existing logic from step09 which calculates xdist
    # from the centroid of the data.
    return step09.spot(header, rows)

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Trust Analysis: Identifying unreliable employee records.")
    print(f"Detected {len(suspicious_indices)} records that may be unreliable.")
    print("-" * 60)
    print("The following records contain input values that deviate significantly")
    print("from the established population norms, making estimates for them")
    print("less trustworthy:")
    
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f"- Record {idx}: High deviation from input norms.")
        
    print("-" * 60)
    print("These records should be reviewed for data entry errors before")
    print("relying on any automated predictions.")
    
    exit(0)
