import csv
from step09 import spot as original_spot

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by detecting outliers in the input 
    columns. A row is considered suspicious if its input values are 
    statistically distant from the median of the dataset.
    
    This implementation reuses the logic from step09.py.
    """
    return original_spot(header, rows)

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

    suspicious_indices = spot(header, rows)
    
    print("Analysis: Detecting configurations far outside observed norms.")
    if not suspicious_indices:
        print("No suspicious configurations found.")
    else:
        print(f"Found {len(suspicious_indices)} configurations that deviate significantly from the norm.")
        print("The most suspicious row indices are:")
        print(suspicious_indices[:5])
        
        top_idx = suspicious_indices[0]
        print(f"\nExample of a suspicious configuration (Row {top_idx}):")
        print(rows[top_idx])
        print("\nThese rows contain input values that are statistically distant from the median,")
        print("suggesting they may be erroneous or outside the range of our previous experience.")
