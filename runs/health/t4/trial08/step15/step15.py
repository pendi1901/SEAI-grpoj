import csv
from step05 import blame as step05_blame

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with poor performance.
    The customer asks which settings can be left at factory defaults; 
    those that do NOT appear in the top culprits for poor performance 
    are the ones that are safe to leave at default.
    """
    # We reuse the logic from step05 which identifies the top 3 features 
    # contributing to 'badness'.
    return step05_blame(header, rows)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Identify all input columns
    input_cols = [name for name in header if not (name.endswith('-') or name.endswith('+'))]
    
    # Get the culprits (the settings that cause poor performance)
    culprits = blame(header, rows)
    
    # Settings that are not culprits are safe to leave at default
    safe_to_default = [col for col in input_cols if col not in culprits]
    
    print("Settings that can be left at factory defaults without hurting performance:")
    for col in safe_to_default:
        print(f"- {col}")
        
    print("\nSettings that significantly impact performance (avoid leaving at default):")
    for col in culprits:
        print(f"- {col}")
        
    exit(0)
