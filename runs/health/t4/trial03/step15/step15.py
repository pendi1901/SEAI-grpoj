import csv
from step05 import blame as base_blame

def blame(header, rows):
    """
    Identifies input columns that best explain the performance of the worst rows.
    We reuse the logic from step05.py which uses a Random Forest to identify
    feature importances relative to the 'badness' of the rows.
    """
    return base_blame(header, rows)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns to float, keep symbolic as is
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    # The customer asks which settings they can leave at factory default.
    # Settings that have low importance in explaining "badness" are safe to leave at default.
    # We identify the most important ones (the ones that cause badness).
    important_settings = blame(header, rows)
    
    # Identify all input columns
    all_inputs = [h for h in header if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Settings that are NOT in the top blame list are the ones safe to leave at default.
    safe_settings = [s for s in all_inputs if s not in important_settings]
    
    print("Settings that are most critical (avoid leaving at default):")
    for s in important_settings:
        print(f"- {s}")
        
    print("\nSettings you can likely leave at factory default without hurting performance:")
    for s in safe_settings:
        print(f"- {s}")
