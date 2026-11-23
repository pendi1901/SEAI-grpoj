import ezr
import step05

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We reuse the logic from step05.py which identifies input factors 
    that significantly correlate with poor performance (high ydist).
    """
    return step05.blame(header, rows)

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify critical factors
    critical_factors = blame(header, rows)
    
    # Identify factors to ignore (all input columns not in critical_factors)
    all_inputs = [col for col in header if not (col.endswith("-") or col.endswith("+"))]
    safe_to_ignore = [f for f in all_inputs if f not in critical_factors]
    
    print("Analysis: Which project factors matter most to cost?")
    print("The following factors are critical and should be monitored closely:")
    for f in critical_factors:
        print(f" - {f}")
        
    print("\nThe following factors have little impact and can be safely ignored:")
    for f in safe_to_ignore:
        print(f" - {f}")
    
    exit(0)
