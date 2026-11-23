import ezr
import step05

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    This reuses the logic from step05.
    """
    return step05.blame(header, rows)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the columns that contribute to poor performance
    blamed_cols = blame(header, rows)
    
    # Identify all input columns
    input_cols = [name for name in header if name[-1] not in "+-!"]
    
    # Settings that can be left at default are those NOT in the blamed list
    safe_defaults = [col for col in input_cols if col not in blamed_cols]
    
    print("Analysis of settings that can be left at factory defaults:")
    if safe_defaults:
        print("The following settings do not significantly impact performance and")
        print("can be left at their default values:")
        for col in safe_defaults:
            print(f" - {col}")
    else:
        print("All input settings appear to have a significant impact on performance.")
        
    exit(0)
