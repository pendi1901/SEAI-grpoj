import ezr
import step05

def blame(header, rows):
    """
    Identify input columns that do not significantly contribute to poor performance.
    We use the logic from step05 to identify 'suspects' (columns that drive bad results).
    The columns NOT in the suspect list are the ones that can be left at defaults.
    """
    # Get the list of columns that DO drive poor performance
    suspects = step05.blame(header, rows)
    
    # Identify all input columns (those not ending in +, -, or !)
    # The header names ending in +, -, or ! are goals.
    inputs = [name for name in header if name[-1] not in "+-!"]
    
    # The columns that can be left at defaults are those that are not suspects
    safe_to_default = [col for col in inputs if col not in suspects]
    
    return safe_to_default

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    safe_settings = blame(header, rows)
    
    print("Analysis of settings that can be left at factory defaults:")
    if safe_settings:
        print("The following settings do not significantly impact performance and can be left at defaults:")
        for s in safe_settings:
            print(f"- {s}")
    else:
        print("All input settings appear to have a significant impact on performance.")
