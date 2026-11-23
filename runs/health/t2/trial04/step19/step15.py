import csv
import step05

def blame(header, rows):
    """
    Returns the names of the input columns that best explain why the worst rows are bad.
    This reuses the logic from step05, which identifies input columns that correlate 
    with poor performance by comparing the distribution of input values in the 
    bottom 10% of rows vs the rest.
    """
    return step05.blame(header, rows)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns to floats, keep strings as is
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    # The customer wants to know which settings they can leave at factory default.
    # Settings that are NOT in the 'blame' list are those that do not strongly 
    # correlate with poor performance, implying they are safe to leave at defaults.
    blamed_cols = blame(header, rows)
    
    input_cols = [h for h in header if h not in ['MRE-', 'ACC+', 'PRED40+']]
    safe_cols = [h for h in input_cols if h not in blamed_cols]
    
    print("Customer Inquiry: Which settings can I leave at factory default without hurting anything?")
    print("Analysis: Settings that do not correlate with poor performance are safe to leave at defaults.")
    print(f"Safe settings to leave at default: {', '.join(safe_cols)}")
    print(f"Settings to be careful with (correlated with poor performance): {', '.join(blamed_cols)}")
