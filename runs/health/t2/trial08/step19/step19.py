import csv
from step09 import spot as original_spot

def spot(header, rows):
    """
    Identifies suspicious rows (outliers) by checking if any input value
    is significantly far from the median of its column.
    This identifies rows that contain values the system has never seen 
    (or are extreme outliers compared to the known distribution).
    """
    # We reuse the logic from step09 which calculates suspicion scores
    # based on distance from the median normalized by the column spread.
    return original_spot(header, rows)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] == 'criterion':
                        processed_row.append(val)
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
        
        suspects = spot(header, rows)
        
        print("Analysis: Identifying configurations with unusual or unseen input settings.")
        if suspects:
            print(f"Found {len(suspects)} suspicious setups.")
            print("The most suspicious row indices (where settings are far from the norm) are:")
            print(suspects[:10])
        else:
            print("No suspicious setups found; all settings appear within expected ranges.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
