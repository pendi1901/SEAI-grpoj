import csv
from step05 import blame as base_blame

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with 'bad' performance.
    The customer asks which settings can be left at defaults without hurting anything.
    By identifying the columns that have the LEAST impact on the 'bad' performance,
    we can infer which settings are safe to leave at default values.
    """
    # Get all input columns
    input_cols = [h for h in header if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Get the columns that cause the most damage (from step05 logic)
    damaging_cols = base_blame(header, rows)
    
    # The columns that are safe are those that are NOT in the damaging list
    safe_cols = [col for col in input_cols if col not in damaging_cols]
    
    return safe_cols

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
            
    safe_settings = blame(header, rows)
    
    print("Settings that can be left at factory defaults without significant impact:")
    print(", ".join(safe_settings))
    print("\nThese columns show the least deviation in the worst-performing setups,")
    print("suggesting they are safe to ignore during optimization.")
