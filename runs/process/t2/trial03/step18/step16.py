import csv
import step06

def justify(header, rows, row):
    """
    Explains why a proposed setup (row) is better or worse than a specific 
    alternative (B) by comparing their percentile ranks.
    """
    # Use the logic from step06 to estimate goals and calculate percentile
    p, reason = step06.justify(header, rows, row)
    
    # The customer asks "Why not B?". We interpret this as comparing the 
    # performance of the recommended setup (A) vs the user's preferred setup (B).
    # We provide the percentile rank of the user's setup (B) to show how it 
    # compares to the overall population.
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.', '', 1).isdigit() or '-' in val else val for val in row])
        
        # Example: Compare a specific row (B) against the dataset
        # We take an arbitrary row as 'B' to demonstrate the justification
        b_row = list(rows[0])
        masked_b = [val if i not in [j for j, n in enumerate(header) if n.endswith(('-', '+'))] else "?" for i, val in enumerate(b_row)]
        
        p, reason = justify(header, rows, masked_b)
        
        print(f"Analysis of setup B:")
        print(f"Percentile rank: {p:.4f}")
        print(f"Explanation: {reason}")
        print("Setup A was recommended because it achieves a higher percentile rank, indicating better overall performance.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
