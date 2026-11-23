import ezr
import step05

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We reuse the logic from step05, which compares the distribution of 
    input values in the worst 25% of rows against the rest of the data.
    """
    return step05.blame(header, rows)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the important factors
    important_factors = blame(header, rows)
    
    # Identify all input columns
    all_inputs = [h for h in header if h[-1] not in "+-!"]
    
    # Determine which can be ignored (those not in important_factors)
    unimportant_factors = [f for f in all_inputs if f not in important_factors]
    
    print("Analysis: Which project facts matter most to cost?")
    print("The following input factors significantly correlate with poor performance:")
    for factor in important_factors:
        print(f"- {factor}")
        
    print("\nYou can safely stop worrying about these factors:")
    for factor in unimportant_factors:
        print(f"- {factor}")
    
    exit(0)
