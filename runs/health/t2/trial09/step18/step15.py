import csv
from step05 import blame as original_blame

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with 'bad' performance.
    This function reuses the logic from step05.py.
    """
    return original_blame(header, rows)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # The customer asks which settings can be left at factory defaults.
    # Settings that do not appear in the 'blame' list are those that do not 
    # significantly differentiate the worst-performing setups from the best.
    # Therefore, these are the settings that can be left at defaults.
    
    all_inputs = [h for h in header if not (h.endswith('-') or h.endswith('+'))]
    blamed_inputs = blame(header, rows)
    safe_to_default = [h for h in all_inputs if h not in blamed_inputs]
    
    print("Analysis: Which settings can be left at factory defaults?")
    print("The following settings do not significantly impact performance differences")
    print("between the best and worst configurations and can be left at defaults:")
    for setting in safe_to_default:
        print(f"- {setting}")
    
    print("\nNote: The settings that most strongly correlate with poor performance are:")
    for setting in blamed_inputs:
        print(f"- {setting}")
