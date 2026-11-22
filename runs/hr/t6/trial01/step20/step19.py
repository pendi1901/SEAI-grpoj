import ezr
import step09

def spot(header, rows):
    """
    Identify rows that are 'untrustworthy' because they are outliers in the 
    input space (x-columns). If a new hire is unlike anyone we have employed,
    our model's estimate for them cannot be trusted.
    """
    # We reuse the logic from step09 which identifies rows that are 
    # furthest from the population centroid in the input feature space.
    return step09.spot(header, rows)

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    suspicious_indices = spot(header, rows)
    
    print("Analysis: When can we not trust our estimates for new hires?")
    print("We cannot trust estimates for employees who are outliers in our input data.")
    print("The following rows represent the most 'unusual' employees in our database:")
    
    for idx in suspicious_indices[:5]:
        row = rows[idx]
        age_idx = header.index('Age')
        role_idx = header.index('jobRole')
        print(f" - Row {idx}: Age {row[age_idx]}, Role {row[role_idx]}")
        
    print("\nLogic: We flag rows that are furthest from the population centroid in the")
    print("input feature space. If a new hire's profile is this far from our")
    print("historical data, our model's predictions for them are unreliable.")
