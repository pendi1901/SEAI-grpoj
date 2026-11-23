import csv
import step01

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Uses the logic from step01 to rank configurations.
    """
    return step01.remember(header, rows)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float, keep symbolic as is
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['criterion']:
                        processed_row.append(val)
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print("The following setups are the most trustworthy (top 5%):")
        for idx in best_indices:
            row = rows[idx]
            # MRE-, ACC+, PRED40+ are indices 0, 1, 2
            print(f"Row {idx:3}: MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
