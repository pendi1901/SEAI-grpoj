import ezr
import step05

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance (high ydist).
    We reuse the logic from step05.py to identify the most impactful settings.
    """
    return step05.blame(header, rows)

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Identify the settings that most influence poor performance
    # These are the settings that, when changed, have the largest impact on ydist.
    # Settings NOT in this list are candidates for being left at factory defaults.
    impactful_settings = blame(header, rows)
    
    # Identify all input columns
    input_cols = [h for h in header if h[-1] not in "+-"]
    
    # Settings that are NOT in the 'impactful' list are safe to leave at defaults
    safe_settings = [h for h in input_cols if h not in impactful_settings]
    
    print("Analysis of settings to leave at factory defaults:")
    print("The following settings have the least impact on performance and")
    print("can likely be left at factory defaults without hurting results:")
    for setting in safe_settings:
        print(f" - {setting}")
        
    print("\nNote: The settings that most influence performance (and should be tuned) are:")
    for setting in impactful_settings:
        print(f" - {setting}")
