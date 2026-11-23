import ezr
import step05

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goals.
    We reuse the logic from step05 to find the most important factors,
    then return the columns that were NOT in the top 3, 
    as these are the ones that have little to do with the outcomes.
    """
    # Get all input column names
    input_cols = [name for name in header if not name.endswith(("+", "-", "!"))]
    
    # Get the most important factors using the logic from step05
    important_factors = step05.blame(header, rows)
    
    # Return the columns that are not in the important list
    # These are the candidates for removal
    unimportant = [name for name in input_cols if name not in important_factors]
    
    return unimportant

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Run the analysis
    unimportant_factors = blame(header, rows)
    
    print("Analysis: Which columns have little impact on employee retention goals?")
    print("Method: Identified columns that do not significantly differentiate")
    print("between the best and worst performing employee records.")
    print(f"\nWe recommend considering the removal of these {len(unimportant_factors)} columns:")
    print(", ".join(unimportant_factors[:10]) + "...")
    print("\nThese columns appear to have the least correlation with our performance goals.")
    
    exit(0)
